'''
This module contains code specific to the DynamoDB service
'''
import boto3
import json

from cloudwatch_dashboards.helpers.util import DEBUG, TAG_NAME, show

CLIENT = boto3.client("dynamodb")
SERVICE_NAME = 'dynamodb'

# pylint: disable=line-too-long

DYNAMODB_METRICS = [
    {'name': "AccountMaxReads"},
    {'name': "AccountMaxTableLevelReads"},
    {'name': "AccountMaxTableLevelWrites"},
    {'name': "AccountMaxWrites"}, 
    {'name': "ConditionalCheckFailedRequests"},
    {'name': "MaxProvisionedTableReadCapacityUtilization"},
    {'name': "MaxProvisionedTableWriteCapacityUtilization"},
    {'name': "OnlineIndexPercentageProgress"},
    {'name': "OnlineIndexThrottleEvents"},
    {'name': "PendingReplicationCount"},
    {'name': "ProvisionedReadCapacityUnits"},
    {'name': "ProvisionedWriteCapacityUnits"},
    {'name': "ReadThrottleEvents"},
    {'name': "ReplicationLatency"},
    {'name': "ReturnedBytes"},
    {'name': "ReturnedItemCount"},
    {'name': "ReturnedRecordsCount"},
    {'name': "SuccessfulRequestLatency"},
    {'name': "SystemErrors"},
    {'name': "ThrottledRequests"},
    {'name': "TimeToLiveDeletedItemCount"},
    {'name': "TransactionConflict"},
    {'name': "UserErrors"},
    {'name': "WriteThrottleEvent"}
]



def get_dashboard_dynamodb(prefix, environment):
    '''
      Reads the tags from the s3 buckets and returns a list of dictionaries.
      Each dict has a key containing the dashboard name, and their values
      have properties that contains a list of all the dynamodb table that
      are tagged with that dashboard name.
    '''
    list_tables_response = CLIENT.list_tables()

    #print('list_tables_response')
    if DEBUG:
        show(list_tables_response)
    ret = []
    tables_by_dashboard = {}
    offset = len(f'{prefix}-{environment}') + 1

    for table_name in list_tables_response['TableNames']:
        if f'{prefix}-{environment}' in table_name:
            if DEBUG:
                print("\n\n\ntable_name", table_name)
            describe_table_response = CLIENT.describe_table(TableName=table_name)

            table_arn = describe_table_response['Table']['TableArn']
            tags = CLIENT.list_tags_of_resource(ResourceArn=table_arn)
            if DEBUG:
                print("tags")
                show(tags)
            dashboard_list = DEFAULT_DASHBOARD_NAME
            for tag in tags['Tags']:
                if DEBUG:
                    print('tag', tag)
                if tag['Key'] == TAG_NAME:
                    dashboard_list = tag['Value']

            if DEBUG:
                print("dashboard_list", dashboard_list)
            for dashboard_name in dashboard_list.split('[ ,;]'):
                if DEBUG:
                    print("dashboard_name", dashboard_name)

                if dashboard_name not in tables_by_dashboard:
                    # make a new dashboard name
                    if DEBUG:
                        print(f"----dynamodb: making a new dashboard object for {dashboard_name}")
                    tables_by_dashboard[dashboard_name] = {
                        'dashboard_type': 'dynamodb',
                        'metric_names': list(map(lambda m: m['name'], DYNAMODB_METRICS)),
                        'names': []
                    }
                tables_by_dashboard[dashboard_name]['names'].append(table_name[offset:])
    if DEBUG:
        print('tables_by_dashboard', json.dumps(tables_by_dashboard, indent=4))
        print('offset', offset)

    for key, value in tables_by_dashboard.items():
        ret.append({key: value})
    return ret
