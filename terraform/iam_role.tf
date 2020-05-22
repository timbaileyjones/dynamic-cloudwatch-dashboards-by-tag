resource "aws_iam_role" "auto_dashboard_config_lambda_execution_role" {
  name = "${var.prefix}-${var.env}-dashboard_config_lambda_execution_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": "AutoDashboardConfigAssumeRole"
    }
  ]
} 
EOF
  tags               = local.tags
}

resource "aws_iam_role" "auto_dashboard_config_cloudwatch_execution_role" {
  name = "${var.prefix}-${var.env}-dashboard_config_cloudwatch_execution_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "events.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": "AutoCloudwatchConfigAssumeRole"
    }
  ]
} 
EOF
  tags               = local.tags
}
