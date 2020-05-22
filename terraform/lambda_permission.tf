resource "aws_lambda_permission" "allow_cloudwatch_to_call_lambda" {
    statement_id = "AllowExecutionFromCloudWatch"
    action = "lambda:InvokeFunction"
    function_name = aws_lambda_function.lambda_function.function_name
    principal = "events.amazonaws.com"
    source_arn = aws_cloudwatch_event_rule.event_s3_trigger.arn
}