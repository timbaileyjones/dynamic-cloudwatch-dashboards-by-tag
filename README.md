# dynamic-cloudwatch-dashboards-by-tag

This repository accompanies a blog article at https://stelligent.com/?p=21529

It shows one possible method of ensuring that every resource for a set of resources is present on at least one Cloudwatch Dashboard, even if that resources was created manually.

It groups like resources together into the same dashboard.
This arbitrary group is driven by the resource having a tag named "CloudwatchDashboardBasenames".  
The value of that tag (is present) is used to compose the dashboard name.
If a resource lacks that tags, then a default tag of 'uncategorized' is applied.  

The resource types supported are:
 * S3 Buckets
 * Lambda Functions
 * API Gateway REST APIs
 * Cloudfront Distributions
 * Dynamodb tables

This repo started life as a CLI program that created these dashboards (and alarms), and it was invoked immediately after running 'terraform apply' in an infrastructure-as-code pipeline.

For the purposes of focus this article on the automation aspectly, I removed the alarm functionality, and lambda-ized the code, so that it responds to Cloudwatch Event Rules, instead of a couple arguments on the command line.

Currently, this repo is incomplete, mostly in that I have not been able to correctly compose the event-rule patterns for the Cloudwatch events for creating/deleting/tagging Lambda/APIGW/CloudFront/Dynamodb. They are defined in `terraform/cloudwatch_event_rule.tf`, but apparently do not yet match events I'm aiming for.

The lambda_handler() function figures out which kind of resource to process, based on the `source` attribute of the incoming event. 

Because of the arbitary grouping aspect of the functionality, all resources of the type have to be read to group their tags, so the rest of the payload isn't used at all.

