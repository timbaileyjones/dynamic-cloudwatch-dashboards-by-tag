resource "aws_iam_policy" "auto_dashboard_config_lambda_execution_policy" {
  name   = "${var.prefix}-${var.env}-dashboard_config_lambda_execution_policy"
  path   = "/"
  policy = data.aws_iam_policy_document.auto_dashboard_config_lambda_execution_policy_document.json
}

