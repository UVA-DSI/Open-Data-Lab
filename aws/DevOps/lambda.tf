provider "aws" {
   region = "us-east-1"
}

// Create Stand Up Lambda Function from Code in S3 Bucket
resource "aws_lambda_function" "stand_up" {
   function_name = "standUp"

   s3_bucket = "odl-code"
   s3_key = "v1.0.0/standUp.zip"

   handler = "main.standUp"
   runtime = "python3.6"

   role = "${aws_iam_role.lambda_exec.arn}"
}

// Create a Stand Down Function from Code in S3 Bucket
resource "aws_lambda_function" "stand_down" {
   function_name = "standDown"

   s3_bucket = "odl-code"
   s3_key = "v1.0.0/standDown.zip"

   handler = "main.standDown"
   runtime = "python3.6"

   role = "${aws_iam_role.lambda_exec.arn}"

}


resource "aws_iam_role" "lambda_exec" {
   name = "EC2_stand_up",
   assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*"
    },
{
"Effect": "Allow",
            "Action": "ec2:DescribeInstances",
            "Resource": "*"
},
{
"Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances",
"ec2:TerminateInstances"
            ],
            "Resource": "arn:aws:ec2:*:*:instance/*",
}
  ]
}
EOF

}




