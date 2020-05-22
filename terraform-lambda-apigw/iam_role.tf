resource "aws_iam_role" "lambda_execution_role" {
  name = "${var.prefix}-${var.env}-serverless_sample_lambda_execution_role"

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
      "Sid": "SampleServerless"
    }
  ]
} 
EOF
  tags               = local.tags
}
