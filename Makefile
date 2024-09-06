install:
	pip install -r requirements.txt

lint:
	flake8 http_utils

format:
	black http_utils

test:
	pytest tests/