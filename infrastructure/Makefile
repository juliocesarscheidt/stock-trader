#!make

ENV?=production
PLAN_FILE?="tfplan"
CLUSTER_NAME?="ecs-cluster"
DOCKER_REGISTRY?=
IMAGE_VERSION?=0.0.1
RABBITMQ_USERNAME?=rabbitmq
RABBITMQ_PASSWORD?=

docker-login:
	-@echo "Docker login"
	aws ecr get-login-password --region $(AWS_DEFAULT_REGION) | \
		docker login --username AWS $(DOCKER_REGISTRY) --password-stdin

docker-build-image:
	-@echo "Building images"
	docker image build --tag $(DOCKER_REGISTRY)/stock-crawler:$(IMAGE_VERSION) ../stock-crawler
	docker image build --tag $(DOCKER_REGISTRY)/stock-api:$(IMAGE_VERSION) ../stock-api
	docker image build --tag $(DOCKER_REGISTRY)/stock-ui:$(IMAGE_VERSION) ../stock-ui

docker-create-repo:
	-@echo "Creating repositories"
	aws ecr describe-repositories --repository-names stock-crawler --region $(AWS_DEFAULT_REGION) || \
		aws ecr create-repository --repository-name stock-crawler --region $(AWS_DEFAULT_REGION)
	aws ecr describe-repositories --repository-names stock-api --region $(AWS_DEFAULT_REGION) || \
		aws ecr create-repository --repository-name stock-api --region $(AWS_DEFAULT_REGION)
	aws ecr describe-repositories --repository-names stock-ui --region $(AWS_DEFAULT_REGION) || \
		aws ecr create-repository --repository-name stock-ui --region $(AWS_DEFAULT_REGION)

push-image: docker-login docker-build-image docker-create-repo
	-@echo "Pushing images"
	docker image push $(DOCKER_REGISTRY)/stock-crawler:$(IMAGE_VERSION)
	docker image push $(DOCKER_REGISTRY)/stock-api:$(IMAGE_VERSION)
	docker image push $(DOCKER_REGISTRY)/stock-ui:$(IMAGE_VERSION)

create-bucket:
	-@echo "Creating bucket"
	aws s3 ls s3://$(AWS_BACKEND_BUCKET) --region $(AWS_DEFAULT_REGION) || \
		aws s3api create-bucket --bucket $(AWS_BACKEND_BUCKET) --region $(AWS_DEFAULT_REGION) \
			--create-bucket-configuration LocationConstraint=$(AWS_DEFAULT_REGION) --acl private

init: create-bucket
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
