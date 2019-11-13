IMAGE_NAME=whos_that_pokemon
TAG=latest

clean:
	rm -rf .pytest_cache/ .coverage

docker-build:
	docker build -t $(IMAGE_NAME):$(TAG) .

docker-tag: docker-build
	docker tag whos_that_pokemon $(IMAGE_NAME):$(TAG)

docker-run:
	docker run -d -p 5000:5000 -e SECURE_KEY $(IMAGE_NAME):$(TAG)

docker-run-it:
	docker run -p 5000:5000 -it $(IMAGE_NAME):$(TAG) bash

test:
	python -m pytest tests/ --cov=pokemon/

lint:
	flake8 pokemon/ tests/

format:
	black pokemon --line-length 79
