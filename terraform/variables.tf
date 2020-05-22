// -----------------------------------------------------------------------------
// Standard Variables
// -----------------------------------------------------------------------------

variable "aws_region" {
  description = "The AWS region in which resources will be defined."
  type        = string
  default     = "us-west-2"
}

variable "sse" {
  description = "The type of Encryption for the bucket"
  type        = string
  default     = "AES256"
}

variable "env" {
  description = "the environment name"
  type        = string
  default     = "dev6"
}

variable "prefix" {
  description = "the first part of all names"
  type        = string
  default     = "timba"
}

locals {
  tags = {
    "owner" : "tim.baileyjones.labs"
    "CloudwatchDashboardBaseNames" : "dashboard_updates"
  }
  account_id         = data.aws_caller_identity.current.account_id
  lambda_sourcepath  = "../src"
  lambda_zipfilename = "../dist/cloudwatch-dashboards-updater.zip"
}
