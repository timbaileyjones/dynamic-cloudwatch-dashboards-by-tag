data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "auto_dashboard_config_lambda_execution_policy_document" {
  statement {
    actions = ["logs:*"]
    resources = [
      #"arn:aws:logs:*"
      "arn:aws:logs:${var.aws_region}:${local.account_id}:*"
    ]
    effect = "Allow"
  }

  statement {
    actions = [
      "cloudfront:ListDistributions",
    ]
    resources = [
      "*"
    ]
    effect = "Allow"
  }
  statement {
    actions = [
      "cloudwatch:ListDashboards",
      "cloudwatch:DeleteDashboards",
      "cloudwatch:PutDashboard"
    ]
    resources = [
      "arn:aws:cloudwatch:*"
    ]
    effect = "Allow"
  }

  statement {
    actions = [
      "s3:ListAllMyBuckets",
      "s3:GetBucketTagging"
    ]
    resources = [
      "arn:aws:s3:::*" # region/account_id don't count in S3
    ]
    effect = "Allow"
  }
  statement {
    actions = [
      "lambda:List*"
    ]
    resources = [
      "*"
    ]
    effect = "Allow"
  }
  statement {
    actions = [
      "apigateway:GET"
    ]
    resources = [
      "*"
    ]
    effect = "Allow"
  }
  statement {
    actions = [
      "dynamodb:ListTables",
      "dynamodb:ListTags",
    ]
    resources = [
      "*"
    ]
    effect = "Allow"
  }
}

data "archive_file" "cloudwatch_dashboard_lambda_zipfile" {
  type        = "zip"
  source_dir  = local.lambda_sourcepath
  output_path = local.lambda_zipfilename
}