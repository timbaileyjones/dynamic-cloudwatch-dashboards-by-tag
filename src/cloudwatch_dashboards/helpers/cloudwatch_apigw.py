'''
    This module contains code specific to the API Gateway service
'''
import os
import boto3
import json


from cloudwatch_dashboards.helpers.util import DEBUG, DEFAULT_DASHBOARD_NAME, TAG_NAME, get_region, show

CLIENT = boto3.client("apigateway")
SERVICE_NAME = 'apigw'

APIGW_METRICS = [
    {'name': '4XXError'},
    {'name': '5XXError'},
    {'name': 'CacheHitCount'},
    {'name': 'CacheMissCount'},
    {'name': 'Count'},
    {'name': 'IntegrationLatency'},
    {'name': 'Latency' }
]


def get_dashboard_apigws(prefix, environment):
    '''
      Similar to `get_dashboard_lambdas`, but for the restapis in the API Gateway service.
    '''
    ret = []

    get_rest_apis_response = CLIENT.get_rest_apis()
    apigws_by_dashboard = {}
    offset = len(f'{prefix}-{environment}') + 1

    for item in get_rest_apis_response['items']:
        rest_id = item['id']
        name = item['name']

        if DEBUG:
            print('item')
            show(item)
        if f'{prefix}-{environment}' in name:
            if DEBUG:
                print("\n\n\nid", rest_id)
                print('name', name)
            arn = f'arn:aws:apigateway:{get_region()}::/restapis/{rest_id}'
            tags = CLIENT.get_tags(resourceArn=arn)
            if DEBUG:
                print("tags")
                show(tags)
            dashboard_list = DEFAULT_DASHBOARD_NAME
            if TAG_NAME not in tags['tags']:
                if DEBUG:
                    print(TAG_NAME, "not found above")
            else:
                dashboard_list = tags['tags'][TAG_NAME]
                
            if DEBUG:
                print("dashboard_list", dashboard_list)
            for dashboard_name in dashboard_list.split('[ ,;]'):
                if DEBUG:
                    print(".1 dashboard_name", dashboard_name)
                if dashboard_name not in apigws_by_dashboard:
                    # make a new dashboard name
                    if DEBUG:
                        print(f"----apigw: making a new dashboard object for {dashboard_name}")
                    apigws_by_dashboard[dashboard_name] = {
                        'dashboard_type': SERVICE_NAME,
                        'metric_names' : list(map(lambda m: m['name'], APIGW_METRICS)),
                        'names' : []
                    }
                apigws_by_dashboard[dashboard_name]['names'].append(name[offset:])


    if DEBUG:
        print('apigws_by_dashboard')
        show(apigws_by_dashboard)
        print('offset', offset)

    for key, value in apigws_by_dashboard.items():
        ret.append({key: value})
    return ret
