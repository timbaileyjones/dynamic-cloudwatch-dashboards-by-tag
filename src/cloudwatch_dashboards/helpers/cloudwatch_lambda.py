'''
This module contains code specific to the lambda service
'''
import boto3
import json

from cloudwatch_dashboards.helpers.util import DEBUG, TAG_NAME, DEFAULT_DASHBOARD_NAME, show

CLIENT = boto3.client("lambda")
SERVICE_NAME = 'lambda'

# pylint: disable=line-too-long

LAMBDA_METRICS = [
    {'name': 'Invocations'},
    {'name': 'Errors'},
    {'name': 'DeadLetterErrors'},
    {'name': 'Duration'},
    {'name': 'Throttles'},
    {'name': 'IteratorAge'},
    {'name': 'ConcurrentExecutions'},
    {'name': 'UnreservedConcurrentExecutions'}
]


def get_dashboard_lambdas(prefix, environment):
    '''
      Reads the tags from the lambdas and returns a list of dictionaries.
      Each dict has a key containing the dashboard name, and their values
      have properties that contains a list of all the lambdas that
      are tagged with that dashboard name.
    '''
    list_functions_response = CLIENT.list_functions()
    ret = []
    lambdas_by_dashboard = {}
    offset = len(f'{prefix}-{environment}') + 1
    for func in list_functions_response['Functions']:
        lambda_func = func['FunctionName']
        if f'{prefix}-{environment}' in lambda_func:
            if DEBUG:
                print("\n\n\nlambda_func", lambda_func)

            dashboard_list = DEFAULT_DASHBOARD_NAME
            try: 
                tags = CLIENT.list_tags(Resource=func['FunctionArn'])
                if DEBUG:
                    print("tags")
                    show(tags)
                if TAG_NAME not in tags['Tags']:
                    tags['Tags'][TAG_NAME] = DEFAULT_DASHBOARD_NAME
            except Exception as exc:
                # If the get_bucket_tagging fails, assume the default
                pass   
                    
            dashboard_list = tags['Tags'][TAG_NAME]
            if DEBUG:
                print("dashboard_list", dashboard_list)
            for dashboard_name in dashboard_list.split('[ ,;]'):
                if DEBUG:
                    print("dashboard_name", dashboard_name)

                if dashboard_name not in lambdas_by_dashboard:
                    # make a new dashboard name
                    if DEBUG:
                        print(f"----lambda: making a new dashboard object for {dashboard_name}")
                        print(map(lambda m: m['name'], LAMBDA_METRICS))
                    lambdas_by_dashboard[dashboard_name] = {
                        'dashboard_type': 'lambda',
                        'metric_names' : list(map(lambda m: m['name'], LAMBDA_METRICS)),
                        'names' : []
                    }
                lambdas_by_dashboard[dashboard_name]['names'].append(lambda_func[offset:])
    if DEBUG:
        print('lambdas_by_dashboard')
        show(lambdas_by_dashboard)
        print('offset', offset)

    for key, value in lambdas_by_dashboard.items():
        ret.append({key: value})
    return ret
