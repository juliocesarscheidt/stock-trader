#!make

ENV?=production
TERRAFORM_PATH?="./infrastructure"
DOCKER_REGISTRY?=
IMAGE_VERSION?=0.0.1

docker-login:
	-@echo "Docker login"
	aws ecr get-login-password --region $(AWS_DEFAULT_REGION) | \
		docker login --username AWS $(DOCKER_REGISTRY) --password-stdin

docker-build-image:
	-@echo "Building images"
	docker image build --tag $(DOCKER_REGISTRY)/stock-crawler:$(IMAGE_VERSION) ./stock-crawler
	docker image build --tag $(DOCKER_REGISTRY)/stock-api:$(IMAGE_VERSION) ./stock-api
	docker image build --tag $(DOCKER_REGISTRY)/stock-ui:$(IMAGE_VERSION) ./stock-ui

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
	$(MAKE) -C $(TERRAFORM_PATH) init

fmt:
	$(MAKE) -C $(TERRAFORM_PATH) fmt

validate:
	$(MAKE) -C $(TERRAFORM_PATH) validate

plan:
	$(MAKE) -C $(TERRAFORM_PATH) plan

apply:
	$(MAKE) -C $(TERRAFORM_PATH) apply

destroy:
	$(MAKE) -C $(TERRAFORM_PATH) destroy
