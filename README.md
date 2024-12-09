master branch is the main branch
you need to create virtual environment for running application

# py -m venv {project-name}

then for activating it
# project-name\Scripts\activate.bat

need to install packages fro that run below command
# pip install -r requirements.txt

go to the clone project directory and run below command to run server
# python manage.py runserver

run migrations for creating database
# python manage.py makemigrations
# python manage.py migrate

for creating super admin use this
# python manage.py createsuperuser
# username: admin
# password: admin

users script for creating users
# python manage.py shell
# from writersapp.models import CustomUser
# user = CustomUser.objects.create_user(username='viewer', email='viewer@example.com', password='viewer', role='viewer')
# user = CustomUser.objects.create_user(username='editor', email='editor@example.com', password='editor', role='editor')
# user = CustomUser.objects.create_user(username='zaeem', email='zaeem@example.com', password='zaeem', role='admin')
# exit()

Admin can use user management and change users roles
Viewer can only view list of books created
Editor can create, view and update books

