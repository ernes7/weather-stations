run1:
	python3 manage.py migrate
	python3 manage.py ingest_data
	python3 manage.py runserver

run0:
	python3 manage.py runserver

clean:
	python3 manage.py flush

test:
	python3 -m pytest -s api/

format:
	black .
	flake8 .
