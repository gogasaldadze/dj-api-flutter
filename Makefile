runserver:
	py manage.py runserver localhost:8000 

migrations:
	py manage.py makemigrations 

migrate:
	py manage.py migrate  

shell:
	py manage.py shell  

sync:
	pip freeze > requirements.txt 
	
install:
	pip install -r requirements.txt 

superuser:
	py manage.py createsuperuser 
	
venv:
	venv/Scripts/activate
	