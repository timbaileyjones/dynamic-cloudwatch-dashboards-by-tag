// ---------------------------------------------------------------------------------------------------------------------
// test S3 Buckets
// ---------------------------------------------------------------------------------------------------------------------
##resource "aws_s3_bucket" "timba-dev-sample-lambda-source-bucket" {
#  bucket = "timba-dev-sample-lambda-source-bucket"
#  tags   = {
#    "CloudwatchDashboardBasenames" = "timba-lambda-code-bucket"
#  }
#}

data "archive_file" "sample_lambda_zip" {
  type        = "zip"
  source_dir  = local.lambda_sourcepath
  output_path = local.lambda_zipfilename
}
