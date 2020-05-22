resource "aws_iam_policy_attachment" "auto_dashboard_config_lambda_execution_policy_attachment" {
  name       = "${var.prefix}-${var.env}-dashboard_config_lambda_execution_policy_attachment"
  roles      = [aws_iam_role.auto_dashboard_config_lambda_execution_role.name]
  policy_arn = aws_iam_policy.auto_dashboard_config_lambda_execution_policy.arn
}

