resource "aws_cloudwatch_event_rule" "event_s3_trigger" {
  name        = "${var.prefix}-${var.env}-event-s3-trigger"
  description = "Capture all cloudwatch create/delete bucket events"

  event_pattern = <<EOF
{
  "detail": {
    "eventName": [
      "DeleteBucket",
      "CreateBucket",
      "DeleteBucketTagging",
      "PutBucketTagging"
    ]
  },
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "source": [
    "aws.s3"
  ]
}
EOF
}


resource "aws_cloudwatch_event_rule" "event_apigateway_trigger" {
  name        = "${var.prefix}-${var.env}-event-apigateway-trigger"
  description = "Capture all cloudwatch create/delete apigateway events"

  event_pattern = <<EOF
{
  "detail": {
    "eventName": [
      "apigateway:DeleteRestApi",
      "apigateway:CreateRestApi"
    ]
  },
  "source": [
    "aws.apigateway"
  ]
}

EOF
}

// lambda
resource "aws_cloudwatch_event_rule" "event_lambda_trigger" {
  name        = "${var.prefix}-${var.env}-event-lambda-trigger"
  description = "Capture all cloudwatch create/delete lambda events"

  event_pattern = <<EOF
{
  "detail": {
    "eventName": [
      "CreateFunction20150331",
      "DeleteFunction20150331",
      "lambda:TagResource",
      "lambda:UntagResource"
    ],
    "eventSource": ["lambda.amazonaws.com"]
  },
  "detail-type": [
    "AWS API Call via CloudTrail"
  ]
}

EOF
}

// dynamodb 

resource "aws_cloudwatch_event_rule" "event_dynamodb_trigger" {
  name        = "${var.prefix}-${var.env}-event-dynamodb-trigger"
  description = "Capture all cloudwatch create/delete dynamodb events"

  event_pattern = <<EOF
{
  "detail": {
    "eventName": [
      "dynamodb:CreateTable",
      "dynamodb:DeleteTable",
      "dynamodb:TagResource",
      "dynamodb:UntagResource"
    ]
  },
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "source": [
    "aws.dynamodb"
  ]
}

EOF
}



resource "aws_cloudwatch_event_rule" "event_cloudfront_trigger" {
  name        = "${var.prefix}-${var.env}-event-cloudfront-trigger"
  description = "Capture all cloudwatch create/delete cloudfront events"

  event_pattern = <<EOF
  {
  "detail": {
    "eventName": [
      "cloudfront:CreateDistribution",
      "cloudfront:CreateDistributionWithTags",
      "cloudfront:CreateStreamingDistribution",
      "cloudfront:CreateStreamingDistributionWithTags", 
      "cloudfront:UpdateDistribution",
      "cloudfront:DeleteDistribution",
      "cloudfront:TagResource",
      "cloudfront:UntagResource"
    ]
  },
  "detail-type": [
    "AWS API Call via CloudTrail"
  ],
  "source": [
    "aws.cloudfront"
  ]
}

EOF
}

