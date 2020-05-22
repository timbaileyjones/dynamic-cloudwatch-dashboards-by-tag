#!/bin/bash
if [ $# -ne 2 ]
then
    echo Usage: $0 bucket-name dashboard-group-name
    exit 1
fi


export bucket=$1
export dashboard_name=$2
aws s3 mb s3://$bucket 
aws s3api put-bucket-tagging --bucket $bucket --tagging TagSet="[{Key=CloudwatchDashboardBasenames,Value=${dashboard_name}}]"

