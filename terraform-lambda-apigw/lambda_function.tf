resource "aws_lambda_function" "example" {
  depends_on = [data.archive_file.cloudwatch_dashboard_lambda_zipfile]


  function_name = "${var.prefix}-${var.env}-sample-lambda"
  role          = aws_iam_role.lambda_exec.arn
  filename      = local.lambda_zipfilename
  handler       = "main.handler"
  runtime       = "nodejs10.x"
  memory_size   = "192"
  timeout       = "360"
  tags          = local.tags
  publish       = true
  source_code_hash = filebase64sha256(local.lambda_zipfilename)
}

 resource "aws_iam_role" "lambda_exec" {
   name = "serverless_example_lambda"

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
       "Sid": ""
     }
   ]
 }
 EOF

 }
