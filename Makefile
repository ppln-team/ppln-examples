APP_NAME=amirassov/ppln-examples
CONTAINER_NAME=ppln-examples

help: ## This help.
	@awk 'BEGIN (FS = ":.*?## ") /^[a-zA-Z_-]+:.*?## / (printf "\033[36m%-30s\033[0m %s\n", $$1, $$2)' $(MAKEFILE_LIST)

build:  ## Build the container
	nvidia-docker build -t $(APP_NAME) .

run: ## Run container
	nvidia-docker run \
		-itd \
		--ipc=host \
		--name=$(CONTAINER_NAME) \
		-v /home/amirassov/data:/data \
		-v $(shell pwd):/ppln $(APP_NAME) bash

exec: ## Run a bash in a running container
	nvidia-docker exec -it $(CONTAINER_NAME) bash

stop: ## Stop and remove a running container
	docker stop $(CONTAINER_NAME); docker rm $(CONTAINER_NAME)

format:
	pre-commit run --all-files
