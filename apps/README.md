# Applications

## Description

- **Core** - holds common modules to be used in other applications
- **Pages** - holds mostly static pages, like home page
- **Quizzes** - responsible for the Quiz and related objects CRUDL
- **Reviews** - responsible for everything about quiz review: submitting, reviewing, rejecting, approving
- **Takes** - responsible for taking quizzes, storing user results and displaying it
- **Users** - contains main user model for project

## Packages
- **django-allauth** - handles everything about user flow: login, logout, sign up, e-mail verification, etc.
- **django-filter** - lives in `*/filters.py`, handles filtering for list views
- **Unidecode** - helps in creating slugs for Quiz model by transliterating its title
