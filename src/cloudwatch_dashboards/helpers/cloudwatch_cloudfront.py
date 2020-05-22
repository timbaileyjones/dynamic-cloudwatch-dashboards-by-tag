'''
This module contains code specific to the cloudfront service
'''
import json

import boto3

from cloudwatch_dashboards.helpers.util import DEBUG, TAG_NAME, DEFAULT_DASHBOARD_NAME, show

SERVICE_NAME = 'cloudfront'
CLIENT = boto3.client(SERVICE_NAME)

# pylint: disable=line-too-long

CLOUDFRONT_METRICS = [
    {'name': "Requests"},
    {'name': "BytesDownloaded"},
    {'name': "BytesUploaded"},
    {'name': "TotalErrorRate"},
    {'name': "4xxErrorRate"},
    {'name': "5xxErrorRate"}
]


def get_dashboard_cloudfront(prefix, environment):
    '''
      Reads the tags from the cloudfront distributions and returns a list of dictionaries.
      Each dict has a key containing the dashboard name, and their values have
      properties that contains a list of all the distributions that
      are tagged with that dashboard name.
    '''
    list_distributions_response = CLIENT.list_distributions()
    if DEBUG:
        print('list_distributions_response')
        show(list_distributions_response)

    ret = []
    cloudfronts_by_dashboard = {}
    if 'Items' not in list_distributions_response['DistributionList']:
        return ret # no cloudfront distributions found
    for dist in list_distributions_response['DistributionList']['Items']:
        cloudfront_dist = None
        matches_prefix_environment = False
        for origin in dist['Origins']['Items']:
            if f'{prefix}-{environment}' in origin['Id']:
                matches_prefix_environment = True
                cloudfront_dist = dist
        if matches_prefix_environment:
            if DEBUG:
                print("\n\n\ncloudfront_dist", cloudfront_dist)
                show(dist)
            tags = CLIENT.list_tags_for_resource(Resource=cloudfront_dist['ARN'])
            if DEBUG:
                print("tags")
                show(tags)

            dashboard_list = DEFAULT_DASHBOARD_NAME
            for item in tags['Tags']['Items']:
                if item['Key'] == TAG_NAME:
                    dashboard_list = item['Value']

            if DEBUG:
                print("dashboard_list", dashboard_list)
            for dashboard_name in dashboard_list.split('[ ,;]'):
                if DEBUG:
                    print("dashboard_name", dashboard_name)

                if dashboard_name not in cloudfronts_by_dashboard:
                    # make a new dashboard name
                    if DEBUG:
                        print(f"----cloudfront: making a new dashboard object for {dashboard_name}")
                    cloudfronts_by_dashboard[dashboard_name] = {
                        'dashboard_type': 'cloudfront',
                        'metric_names' : list(map(lambda m: m['name'], CLOUDFRONT_METRICS)),
                        'names' : []
                    }
                dist_id = dist['Id']
                if DEBUG:
                    print('dist_id', dist_id)
                cloudfronts_by_dashboard[dashboard_name]['names'].append(dist_id)
    if DEBUG:
        print('cloudfronts_by_dashboard')
        show(cloudfronts_by_dashboard)

    for key, value in cloudfronts_by_dashboard.items():
        ret.append({key: value})
    return ret
