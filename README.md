# WSGI-Framework
Web-framework with ORM 🌍

To launch application you should make several steps:

1. Create a virtual environment
## python -m venv venv

2. Activate virtual environment
## source venv/bin/activate

3. Install requirements
## pip install -r requirements.txt

4. Launch gunicorn to serve application
## gunicorn run:app -b 0.0.0.0:8080
