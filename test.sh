#!/bin/bash
export PATH=$PATH:/usr/local/bin/:/home/tim/.local/bin/

./deploy.sh

prefix=`grep  -A 3 prefix terraform/variables.tf | grep default  | cut -f2 -d'"'`
env=`grep  -A 3 env terraform/variables.tf | grep default  | cut -f2 -d'"'`
aws lambda --region us-west-2 invoke --function-name ${prefix}-${env}-config_dashboards_updater --payload file://tests/bucket_put_event.json output

cat output
