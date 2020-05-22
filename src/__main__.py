
'''
   main entrypoint for invoking from a zip file:
      python3 cloudwatch_dashboards.zip
'''

import json
import os
import sys

from cloudwatch_dashboards.cloudwatch_dashboards import update_dashboards
from cloudwatch_dashboards.helpers.util import show

print("sys.argv", sys.argv)

if len(sys.argv) < 2:
    print("Usage: cloudwatch_dashboards.py event.json")
    sys.exit(1)

event = json.loads(open(sys.argv[1]).read())
response = update_dashboards(event)
show(response)
