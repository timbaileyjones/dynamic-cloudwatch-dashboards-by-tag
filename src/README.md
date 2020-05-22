# cloudwatch-dashboards
https://git.sami.int.thomsonreuters.com/wm-terraform-modules-aws/acme-cloudwatch-dashboards



## Installing
Assuming a python3 runtime is available:
```
    pip install -r requirements.txt
```

## Configuration

In the `./lib` directory are several service-specific files:
 * cloudwatch_apigw.py
 * cloudwatch_cloudfront.py
 * cloudwatch_dynamodb.py
 * cloudwatch_lambda.py
 * cloudwatch_s3.py

In each of these source files is a global array ending in `_METRICS`.  This array contains the metrics we're going to track in Cloudwatch Dashboards.



## Manual Usage 

This is a python script to idempotently create a set of dashboards in Cloudwatch, each graphing an arbitrary number of lambdas.

It can be run over and over again, without a need to delete the dashboards between runs.  This is because CloudWatch's put_dashboard function will create OR update a dashboard as required.

A delete function is also provided for easy cleanup.

### Creating Cloudwatch dashboards
 * set AWS_DEFAULT_PROFILE and AWS_DEFAULT_REGION appropriately
 * run 
   ```
   python3 ./cloudwatch-dashboards.py create $ENVIRONMENT`
   ```

### Deleting Cloudwatch dashboards
 * set AWS_DEFAULT_PROFILE and AWS_DEFAULT_REGION appropriately
 * run 
   ```
   python3 ./cloudwatch-dashboards.py delete $ENVIRONMENT
   ```

## Internal Documentation - Code Walk-through

 * `lib/dashboard.py`

    * `get_dashboard_lambdas()` 

       Reads the tags from the lambdas and returns a list of dictionaries.  Each dict has a key containing the dashboard name, and their values have properties that contains a list of all the lambdas that are tagged with that dashboard name.

    * `get_dashboard_apigws()`

      Similar to `get_dashboard_lambdas`, but for the restapis in the API Gateway service.

    * `create_dashboard()`

      Creates a Cloudwatch Dashboard for one such element returned from `get_dashboard_lambdas()` and `get_dashboard_apigws()`

    * `delete_dashboard()`

      Deletes a Cloudwatch Dashboard 

The main script uses the above functions in the following manner:
  * checks arguments for validity
  * gets all the dashboard definition for lambdas, using `get_dashboard_lambdas()`.
  * gets all the dashboard definition for APIGWs, using `get_dashboard_apigws()`
  * combines the two lists
  * a for loop calls `create_dashboard()` or `delete_dashboard()` for each dashboard, depending upon which operation was specified on the command line.


Github issue link about getting inconsistent plan output:
    https://github.com/terraform-aws-modules/terraform-aws-eks/issues/527#issuecomment-626878507