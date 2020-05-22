#!/usr/bin/env python3
"""
    This program generates dashboards for the following 5 services:
     * `apigateway`
     * `cloudfront`
     * `dynamodb`
     * `lambda`
     * `s3`
    For each service, it a methods in each service's helpers/cloudwatch-*.py file:
     * `get_dashboard_<service_name>`
    collecting dashboards definitions into an array.
    These `get_dashboard_*` methods could not be genericized
    because of the inconsistencies in the boto3
    method names and the response payloads.

    Then it spins through a loop for the dashboards, actually
    creating or deleting the CW objects (fortuntely, this part is quite generic).

"""
# pylint: disable=invalid-name
# pylint: disable=broad-except
import json

from cloudwatch_dashboards.helpers.update_dashboards import update_dashboards
from cloudwatch_dashboards.helpers.util import show

def lambda_handler(event, _):
    '''
       normal lambda entrypoint
    '''
    messages = []
    show(event)
    ret = {'messages': messages}
    try:
        ret['result'] = update_dashboards(event)
    except Exception as exc:
        print("Caught exception %s" % str(exc))
        ret['result'] = "Caught exception %s" % str(exc)
    return ret
