# Django Quiz App
## Description
I do not even know where to start. The idea is simple and straightforward - a quiz application in Django. The main goal is to make the project as simple and understandable as possible, but at the same time fit the skills that are indicated in my resume.

If by chance you're a recruiter, or you're just curious, [you can get a look at the project in action here](https://django-quiz-app.site/).

## Running locally
If you want to run this project locally, just follow this steps:

 1. Clone this repository to any desirable place on your PC
 2. Create virtual environment, activate it and install requirements via `pip install -r requirements/dev.txt`
 3. Create `.env` file in `config/settings/` folder

> Use .env.example as a guideline to setting .env up; however, while most of the settings in .env are required in production, for local development you only need to specify SECRET_KEY
4. Run `python manage.py migrate`; If anything goes wrong - make sure you did every previous step correctly
5. Create superuser via `python manage.py createsuperuser`
6. Run server via `python manage.py runserver` and proceed to localhost:8000

If you have troubles running this project locally - please open an issue.
