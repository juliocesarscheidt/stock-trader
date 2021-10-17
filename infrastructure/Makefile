#!make

ENV?=production
PLAN_FILE?="tfplan"
CLUSTER_NAME?="ecs-cluster"
DOCKER_REGISTRY?=
IMAGE_VERSION?=0.0.1
RABBITMQ_USERNAME?=rabbitmq
RABBITMQ_PASSWORD?=

init:
	-@echo "Init"
	terraform init -upgrade=true \
		-backend-config="bucket=$(AWS_BACKEND_BUCKET)" \
		-backend-config="key=state.tfstate" \
		-backend-config="region=$(AWS_DEFAULT_REGION)" \
		-backend-config="workspace_key_prefix=terraform/$(CLUSTER_NAME)" \
		-backend-config="access_key=$(AWS_ACCESS_KEY_ID)" \
		-backend-config="secret_key=$(AWS_SECRET_ACCESS_KEY)" \
		-backend-config="encrypt=true"

	-@terraform workspace new development 2> /dev/null
	-@terraform workspace new production 2> /dev/null
	terraform workspace select $(ENV)

	make plan

fmt:
	terraform fmt -write=true -recursive

validate:
	terraform validate

plan: validate
	-@echo "Plan"
	terraform plan \
		-out=$(PLAN_FILE) \
		-var-file=$(ENV).tfvars \
		-var aws_region="$(AWS_DEFAULT_REGION)" \
		-var docker_registry="$(DOCKER_REGISTRY)" \
		-var cluster_name="$(CLUSTER_NAME)" \
		-var image_version="$(IMAGE_VERSION)" \
		-var rabbitmq_username="$(RABBITMQ_USERNAME)" \
		-var rabbitmq_password="$(RABBITMQ_PASSWORD)" \
		-input=false

apply: plan
	-@echo "Apply"
	terraform apply $(PLAN_FILE)
	terraform output -json

destroy: plan
	-@echo "Destroy"
	terraform destroy \
		-var-file=$(ENV).tfvars \
		-auto-approve
