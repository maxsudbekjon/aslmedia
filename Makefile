udb:
	rm -rf film/migrations/*
	rm -rf user/migrations/*
	touch film/migrations/__init__.py
	touch user/migrations/__init__.py
	python3 manage.py makemigrations
	python3 manage.py migrate


