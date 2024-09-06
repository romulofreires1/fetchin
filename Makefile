install:
	pip install -r requirements.txt

lint:
	flake8 src/http_helper

format:
	black src/http_helper

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

build:
	python -m build

publish-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

publish:
	twine upload dist/*

# Limpar arquivos temporários de build
clean:
	rm -rf dist/ build/ *.egg-info