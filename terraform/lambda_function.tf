resource "aws_lambda_function" "lambda_function" {
  depends_on = [data.archive_file.cloudwatch_dashboard_lambda_zipfile]


  function_name = "${var.prefix}-${var.env}-config_dashboards_updater"
  role          = aws_iam_role.auto_dashboard_config_lambda_execution_role.arn
  filename      = local.lambda_zipfilename
  handler       = "cloudwatch_dashboards.cloudwatch_dashboards.lambda_handler"
  runtime       = "python3.7"
  memory_size   = "192"
  timeout       = "360"
  tags          = local.tags
  publish       = true
  source_code_hash = filebase64sha256(local.lambda_zipfilename)
  environment {
    variables = {
      "DEBUG" = "1"
      "PREFIX" = var.prefix
      "ENVIRONMENT" = var.env
    }
  }
}

#
# to prevent the lambda from being executed concurrently
#

resource "aws_lambda_provisioned_concurrency_config" "lambda_function" {
  function_name                     = aws_lambda_function.lambda_function.function_name
  provisioned_concurrent_executions = 1
  qualifier                         = aws_lambda_function.lambda_function.version
}

