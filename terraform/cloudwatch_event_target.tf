resource "aws_cloudwatch_event_target" "s3_to_lambda_target" {
  arn       = aws_lambda_function.lambda_function.arn 
  rule      = aws_cloudwatch_event_rule.event_s3_trigger.name
}
resource "aws_cloudwatch_event_target" "apigateway_to_lambda_target" {
  arn       = aws_lambda_function.lambda_function.arn 
  rule      = aws_cloudwatch_event_rule.event_apigateway_trigger.name
}
resource "aws_cloudwatch_event_target" "lambda_to_lambda_target" {
  arn       = aws_lambda_function.lambda_function.arn 
  rule      = aws_cloudwatch_event_rule.event_lambda_trigger.name
}
resource "aws_cloudwatch_event_target" "dynamodb_to_lambda_target" {
  arn       = aws_lambda_function.lambda_function.arn 
  rule      = aws_cloudwatch_event_rule.event_dynamodb_trigger.name
}
resource "aws_cloudwatch_event_target" "cloudfront_to_lambda_target" {
  arn       = aws_lambda_function.lambda_function.arn 
  rule      = aws_cloudwatch_event_rule.event_cloudfront_trigger.name
}