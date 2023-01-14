# run:
# 	poetry run python3 src/app.py

run:
	python3 -m src.app

test:
	python3 -m pytest src

celery:
	celery -A app.celery worker --loglevel=DEBUG
