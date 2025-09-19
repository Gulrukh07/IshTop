mig:
	python3 manage.py makemigrations
	python3 manage.py migrate
user:
	python3 manage.py createsuperuser

app:
	python3 manage.py startapp apps

run:
	 daphne -b 0.0.0.0 -p 8000 root.asgi:application
