#!make

build:
	docker image build \
		--tag stock-api:latest \
		--file Dockerfile .

lint-app:
	docker container run --rm \
		--name stock-api-lint \
		-v $$(pwd):/usr/src/app \
		-w /usr/src/app \
		--entrypoint "" \
		cytopia/black:latest-0.2 sh -c "black --check -v ."

test-app:
	@echo "Missing tests"
