run:
	@python manage.py runserver 8000

makemigrate:
	@python manage.py makemigrations

migrate:
	@python manage.py migrate

test:
	@python manage.py test