'''
This module contains code specific to the s3 service
'''
import boto3
import json

from cloudwatch_dashboards.helpers.util import DEBUG, TAG_NAME, DEFAULT_DASHBOARD_NAME, show

CLIENT = boto3.client("s3")
SERVICE_NAME = 's3'

# pylint: disable=line-too-long

BUCKET_METRICS = [
    {'name': 'BucketSizeBytes'},
    {'name': 'NumberOfObjects'},
    {'name': 'AllRequests'},
    {'name': 'GetRequests'},
    {'name': 'PutRequests'},
    {'name': 'DeleteRequests'},
    {'name': 'HeadRequests'},
    {'name': 'PostRequests'},
    {'name': 'SelectRequests'},
    {'name': 'SelectScannedBytes'},
    {'name': 'SelectReturnedBytes'},
    {'name': 'ListRequests'},
    {'name': 'BytesDownloaded'},
    {'name': 'BytesUploaded'},
    {'name': '4xxErrors'},
    {'name': '5xxErrors'},
    {'name': 'FirstByteLatency'},
    {'name': 'TotalRequestLatency'}
]


def get_dashboard_s3(prefix, environment):
    '''
      Reads the tags from the s3 buckets and returns a list of dictionaries.
      Each dict has a key containing the dashboard name, and their values
      have properties that contains a list of all the buckets that
      are tagged with that dashboard name.
    '''
    list_buckets_response = CLIENT.list_buckets()
    ret = []
    buckets_by_dashboard = {}
    offset = len(f'{prefix}-{environment}') + 1
    show(list_buckets_response)
    for bucket in list_buckets_response['Buckets']:
        bucket_name = bucket['Name']
        if f'{prefix}-{environment}' in bucket_name:
            if DEBUG:
                print("\n\n\nbucket_name", bucket_name)

            dashboard_list = DEFAULT_DASHBOARD_NAME
            try: 
                tags = CLIENT.get_bucket_tagging(Bucket=bucket_name)
                if DEBUG:
                    print("tags")
                    show(tags)
                for tag in tags['TagSet']:
                    if DEBUG:
                        print('tag', tag)
                    if tag['Key'] == TAG_NAME:
                        dashboard_list = tag['Value']
            except Exception as exc:
                # If the get_bucket_tagging fails, assume the default
                pass   

            if DEBUG:
                print("dashboard_list", dashboard_list)
            for dashboard_name in dashboard_list.split('[ ,;]'):
                if DEBUG:
                    print("dashboard_name", dashboard_name)

                if dashboard_name not in buckets_by_dashboard:
                    # make a new dashboard name
                    if DEBUG:
                        print(f"----s3: making a new dashboard object for {dashboard_name}")
                    buckets_by_dashboard[dashboard_name] = {
                        'dashboard_type': 's3',
                        'metric_names' : list(map(lambda m: m['name'], BUCKET_METRICS)),
                        'names' : []
                    }
                buckets_by_dashboard[dashboard_name]['names'].append(bucket_name[offset:])
        else:
            if DEBUG:
                print("skipping bucket_name", bucket_name)
    if DEBUG:
        print('buckets_by_dashboard') 
        show(buckets_by_dashboard)
        print('offset', offset)

    for key, value in buckets_by_dashboard.items():
        ret.append({key: value})
    return ret
