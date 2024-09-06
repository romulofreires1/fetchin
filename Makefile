install:
	pip install -r requirements.txt

lint:
	flake8 http_utils

format:
	black http_utils

test:
	pytest -v -s tests/

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-build:
	docker-compose build

docker-logs:
	docker-compose logs -f

play:
	python playground.py 