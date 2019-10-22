IMAGE_NAME=whos_that_pokemon
TAG=latest

docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) .

docker-tag:
	docker tag whos_that_pokemon $(IMAGE_NAME):$(TAG)

docker-run:
	docker run -d -p 5000:5000 -e SECURE_KEY $(IMAGE_NAME):$(TAG)

docker-run-it:
	docker run -p 5000:5000 -it $(IMAGE_NAME):$(TAG) bash

test:
	python -m pytest tests/ --cov=pokemon/

lint:
	python -m pylint pokemon/
