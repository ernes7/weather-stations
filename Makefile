run1:
	python manage.py ingest_data
	python manage.py runserver

run0:
	python manage.py runserver

clean:
	python manage.py flush

test:
	python -m pytest -s api/

format:
	black .
	flake8 .