// ---------------------------------------------------------------------------------------------------------------------
// test S3 Buckets
// ---------------------------------------------------------------------------------------------------------------------
resource "aws_s3_bucket" "timba-dev6-test-log-bucket-1" {
  bucket = "timba-dev6-test-log-bucket-1"
  tags   = {
    "CloudwatchDashboardBasenames" = "timba-log-buckets"
  }
}
resource "aws_s3_bucket" "timba-dev6-test-log-bucket-2" {
  bucket = "timba-dev6-test-log-bucket-2"
  tags   = {
    "CloudwatchDashboardBasenames" = "timba-log-buckets"
  }
}
resource "aws_s3_bucket" "timba-dev6-test-data-bucket-2" {
  bucket = "timba-dev6-test-data-bucket-1"
  tags   = {
    "CloudwatchDashboardBasenames" = "timba-data-buckets"
  }
}
resource "aws_s3_bucket" "timba-dev6-test-data-bucket-1" {
  bucket = "timba-dev6-test-data-bucket-2"
  tags   = {
    "CloudwatchDashboardBasenames" = "timba-data-buckets"
  }
}
