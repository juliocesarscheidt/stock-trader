#!/bin/bash

set -ex

export AWS_BUCKET_NAME="stock-trader-$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 12 | head -n1)"
export AWS_REGION=${AWS_DEFAULT_REGION:-"sa-east-1"}

# create the bucket
aws s3 mb "s3://${AWS_BUCKET_NAME}" --region "${AWS_REGION}"
# build the application
rm -rf "$(pwd)/dist/" && yarn install && yarn build
# copy static files
aws s3 cp --recursive "$(pwd)/dist/" "s3://${AWS_BUCKET_NAME}/" --region "${AWS_REGION}"
# enable website static hosting on bucket
aws s3 website "s3://${AWS_BUCKET_NAME}" --index-document index.html
# create a policy file to allow public read on bucket objects
cat > policy.json <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
          "s3:GetObject"
      ],
      "Resource": [
        "arn:aws:s3:::${AWS_BUCKET_NAME}/*"
      ]
    }
  ]
}
EOF
# apply the policy on bucket
aws s3api put-bucket-policy --bucket "${AWS_BUCKET_NAME}" --policy file://policy.json

echo "[INFO] Website deployed on :: http://${AWS_BUCKET_NAME}.s3-website-${AWS_REGION}.amazonaws.com"
