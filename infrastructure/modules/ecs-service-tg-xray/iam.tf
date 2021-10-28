resource "aws_iam_role" "ecs-task-role" {
  name               = "ecs-task-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": [
          "ecs.amazonaws.com",
          "ecs-tasks.amazonaws.com"
        ]
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "ecs-xray-task-role-policy-attachment" {
  role       = aws_iam_role.ecs-task-role.id
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}

# resource "aws_iam_role_policy" "ecs-xray-task-role-policy" {
#   name   = "ecs-xray-task-role-policy"
#   role   = aws_iam_role.ecs-task-role.id
#   policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Action": [
#         "xray:PutTraceSegments",
#         "xray:PutTelemetryRecords",
#         "xray:GetSamplingRules",
#         "xray:GetSamplingTargets",
#         "xray:GetSamplingStatisticSummaries"
#       ],
#       "Resource": [
#         "*"
#       ]
#     }
#   ]
# }
# EOF
# }
