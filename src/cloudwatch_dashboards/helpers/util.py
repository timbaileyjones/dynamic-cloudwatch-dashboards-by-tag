'''
    utilities and constants
'''

import json
import os

import boto3

DEBUG = os.getenv("DEBUG") is not None

TAG_NAME = "CloudwatchDashboardBasenames"
DEFAULT_DASHBOARD_NAME = "uncategorized"

SERVICE_TYPE = {
    "lambda": "AWS/Lambda",
    "apigw": "AWS/ApiGateway",
    "dynamodb": "AWS/DynamoDB",
    "cloudfront": "AWS/CloudFront",
    "s3": "AWS/S3"
}
OBJECT_TYPE = {
    "lambda": "FunctionName",
    "apigw": "ApiName",
    "dynamodb": "TableName",
    "cloudfront": "DistributionId",
    "s3": "BucketName"
}

sts_client = boto3.client('sts')
CALLER_IDENTITY = sts_client.get_caller_identity()

def get_account_id():
    if 'Account' in CALLER_IDENTITY:
        return CALLER_IDENTITY['Account']
    return 'uninitialized' 

def get_region():
    return os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", 'uninitialized'))

def show(obj):
    '''
        convenience method to display AWS responses but
        without the annoying "ResponseMetadata" element.
    '''
    rmd = "ResponseMetadata"
    if rmd in obj:
        del obj[rmd]
    print(json.dumps(obj, indent=4, default=str).replace('\n', "\n\u00A0")) 