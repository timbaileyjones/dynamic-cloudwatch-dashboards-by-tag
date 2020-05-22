
import json
import os

from cloudwatch_dashboards.helpers.create_delete_dashboards import create_dashboard, delete_dashboard, get_existing_dashboards
from cloudwatch_dashboards.helpers.cloudwatch_lambda import get_dashboard_lambdas
from cloudwatch_dashboards.helpers.cloudwatch_apigw import get_dashboard_apigws
from cloudwatch_dashboards.helpers.cloudwatch_dynamodb import get_dashboard_dynamodb
from cloudwatch_dashboards.helpers.cloudwatch_cloudfront import get_dashboard_cloudfront
from cloudwatch_dashboards.helpers.cloudwatch_s3 import get_dashboard_s3

from cloudwatch_dashboards.helpers.util import DEBUG, show

SOURCE_MAPPINGS = {
    'aws.lambda': get_dashboard_lambdas, 
    'aws.apigateway': get_dashboard_apigws, 
    'aws.dynamodb': get_dashboard_dynamodb, 
    'aws.cloudfront': get_dashboard_cloudfront, 
    'aws.s3': get_dashboard_s3
}
DASHBOARD_TYPE_MAPPINGS = {
    'aws.lambda': 'lambda', 
    'aws.apigateway': 'apigw',  # this one is different
    'aws.dynamodb': 'dynamodb', 
    'aws.cloudfront': 'cloudfront', 
    'aws.s3': 's3'
}

def update_dashboards(event):
    prefix = os.getenv("PREFIX", "timba")  # from the environment sections of terraform/lambda_function.tf
    environment = os.getenv("ENVIRONMENT", "none")  # from the environment sections of terraform/lambda_function.tf
    show(event) 

    source = event['source']
    if source not in SOURCE_MAPPINGS:
        return {'message', f'unknown source: "{source}"'}

    dashboard_type = DASHBOARD_TYPE_MAPPINGS[source]

    new_dashboards = SOURCE_MAPPINGS[source](prefix, environment) 
    remaining_dashboards = get_existing_dashboards(prefix, environment)
    original_remaining_dashboard_count = len(remaining_dashboards)
    if DEBUG:
        print('original_remaining_dashboard_count', original_remaining_dashboard_count)
        print('remaining_dashboards')
        show(remaining_dashboards)

    for dashboard in new_dashboards:
        if DEBUG:
            print("dashboard", type(dashboard))
            show(dashboard)
        for dashboard_name, details in dashboard.items():
            names = details["names"]
            metric_names = details["metric_names"]
            dashboard_type = details["dashboard_type"]

            create_dashboard(
                prefix=prefix,
                environment=environment,
                dashboard_type=dashboard_type,
                metric_names=metric_names,
                basename=dashboard_name,
                names=names,
            )
            # remove current dashboard from list of remaining dashboards, 
            # so we can delete them at the end of the this loop
            remaining_dashboards = list(filter(lambda x: x != f'{prefix}-{environment}-{dashboard_name}-{dashboard_type}', remaining_dashboards))

    deleted_dashboard_count = 0
    for remaining_dashboard in remaining_dashboards:
        # only delete if it has the same suffix/dashboard_type 
        # as the service we're handling. 
        if remaining_dashboard.endswith(f'-{dashboard_type}'):  
            delete_dashboard(remaining_dashboard)
            deleted_dashboard_count = deleted_dashboard_count + 1

    return  {
        'new_dashboard_count': len(new_dashboards),
        'original_dashboard_count': original_remaining_dashboard_count,
        'remaining_dashboards': len(remaining_dashboards),
        'deleted_dashboard_count': deleted_dashboard_count
    }