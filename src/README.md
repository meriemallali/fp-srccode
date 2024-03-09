# Collaboration Web Application

This application is a collaboration web platform developed using Django, Django Rest Framework, django-channels, Django redis, Daphne, Bootstrap 5, CSS3, and SQLite3. 
It features user authentication, todos creation and updates, task management, and real-time chat functionality.

## System Requirements

- Python version 3.11.3

## Getting Started

To run the application, please follow these steps:

1. Install the virtual environment:
   py -m venv venv

2. Activate the virtual environment: 
   Browse into the scripts folder inside the virtualenv folder it can be "scripts" or "Scripts".
   venv\Scripts\activate 

3. Browse to the Django project folder 'src' (where the manage.py file is located ):
   1. Install the requirements.txt file: 
   pip install -r requirements.txt
   2. Run the server, specify the port number (optional):
   py manage.py runserver 
   

4.  To run the tests: 
   py manage.py test
