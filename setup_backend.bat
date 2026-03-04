python -m venv venv
call venv\Scripts\activate.bat
pip install django djangorestframework psycopg2 django-cors-headers pytest-django djangorestframework-simplejwt
django-admin startproject tunningtracker_backend
