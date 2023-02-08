run:
	python3 -m manage

test:
	python3 -m pytest

celery:
	celery -A src.server.celeryu worker --loglevel=DEBUG


coverage:
	coverage run -m pytest

html:
	coverage html
