'''
   generic functions for creating and deleting dashboards
'''
import os

import boto3
import json   # because json doesn't support embedded dates

from cloudwatch_dashboards.helpers.util import DEBUG, SERVICE_TYPE, OBJECT_TYPE, TAG_NAME , get_account_id, get_region, show

CLIENT = boto3.client("cloudwatch")

DEBUG = os.getenv("DEBUG") is not None


DURATIONS = [5, 60, 1440]

def _create_metric(metric_name, dashboard_type, prefix, environment, name):
    '''
    a local-only helper function to construct the most detailed
    portion of the cloudwatch dashboard_body object.
    '''
    metric = []
    metric.append(SERVICE_TYPE[dashboard_type])
    metric.append(metric_name)
    #
    # metrics for cloudfront require six strings, most others just four.
    # and they MUST be in this position.  Do not change the order of the .append() calls
    #
    if dashboard_type == 'cloudfront':
        metric.append('Region')
        metric.append('Global')
    metric.append(OBJECT_TYPE[dashboard_type])

    if dashboard_type == 'cloudfront':
        metric.append(name)
    else:
        metric.append(f"{prefix}-{environment.lower()}-{name}")

    #
    # metrics for s3 require six strings, most others just four.
    # the additional fields for s3 must be at the end.
    #
    if dashboard_type == 's3':
        metric.append('FilterId')
        metric.append('EntireBucket')
    return metric

def get_existing_dashboards(prefix, environment): 
    return list(map(lambda x: x['DashboardName'], CLIENT.list_dashboards()['DashboardEntries']))


def _create_metrics(metric_name, dashboard_type, prefix, environment, lambda_list):
    '''
    a second local-only helper function to construct the most detailed
    portion of the cloudwatch dashboard_body object.
    '''
    return list(map(lambda name:
                    _create_metric(metric_name, dashboard_type, prefix, environment, name),
                    lambda_list))

def create_dashboard(*, prefix, environment, metric_names, dashboard_type, basename, names):
    '''
      Creates a Cloudwatch Dashboard for one such element returned
      from `get_dashboard_lambdas()` and `get_dashboard_apigws()`
    '''
    row_number = 0
    dashboard_name = f"{prefix}-{environment.lower()}-{basename}-{dashboard_type}"
    print(f"create_dashboard({dashboard_name})... ", end='')
    widgets = []
    #
    #  put in a descriptor
    #
    descriptor = {"type": "text",
                  "x": 0,
                  "y": row_number,
                  "width": len(DURATIONS) * 8,
                  "height": 2,
                  "properties": {"markdown": "\n# "+ dashboard_name +"\n"}
                 }
    widgets.append(descriptor)
    #
    #  add a graph for each metric_name
    #
    col_number = 0
    for duration in DURATIONS:
        row_number = 0
        for metric_name in metric_names:
            metrics = _create_metrics(metric_name, dashboard_type, prefix, environment, names)
            widget = {
                'type': 'metric',
                'x': col_number,
                'y': row_number,
                'width': 8,
                'height': 6,
                'properties': {
                    'title': f'{metric_name}-{duration}m',
                    # multiple lambdas on each graph
                    'metrics': metrics,
                    'period': duration * 60,
                    'stat': 'Maximum',
                    'region': os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
                }
            }
            widgets.append(widget)
            row_number += 1
        col_number += 8

    dashboard_body = {'widgets' : widgets}
    dashboard_body_j = json.dumps(dashboard_body)
    response = CLIENT.put_dashboard(DashboardName=dashboard_name,
                                    DashboardBody=dashboard_body_j)
    show(response)

    print('created!')

    if DEBUG:
        print(f'dashboard_body for {dashboard_name}')
        show(dashboard_body)

def delete_dashboard(dashboard_name):
    '''
      Deletes a Cloudwatch Dashboard
    '''
    print("deleting", dashboard_name)
    response = CLIENT.delete_dashboards(DashboardNames=[dashboard_name])
    show('delete_dashboards returns')
    show(response)
