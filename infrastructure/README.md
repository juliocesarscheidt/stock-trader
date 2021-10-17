## Deploy IaC

In order to deploy, run the following commands:

```bash
export ENV="production"
# aws settings
export AWS_ACCESS_KEY_ID="$AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="$AWS_SECRET_ACCESS_KEY"
export AWS_DEFAULT_REGION="$AWS_DEFAULT_REGION"
# S3 bucket for terraform backend
export AWS_BACKEND_BUCKET="backend-bucket-$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 12 | head -n1)"
# application settings
export DOCKER_REGISTRY="000000000000.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
export CLUSTER_NAME="ecs-cluster"
export IMAGE_VERSION="0.0.1"
# rabbitmq settings
export RABBITMQ_USERNAME="rabbitmq"
export RABBITMQ_PASSWORD="$(cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 16 | head -n1)"

# login into the ECR, build the image, creates the repository (if doesn't exist) and pushes the image to the repository
make push-image

# create the backend bucket on S3 (if doesn't exist, this could take a few minutes), initializes the terraform, create the workspaces, validate and do the plan
make init

# apply the previous plan
make apply
```
