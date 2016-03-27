# Your-Opinion-Matters-Django-
A voting app to create polls and give ur opinion about other polls.

How to install and run the app.

1. Install django

2. install south (migration manager)

3. create your database

4. add south to INSTALLED_APPS

5. run syncdb, this will add the django and south tables to the database

6. add the mydj app in INSTALLED_APPS in settings.py

7. run "python manage.py schemamigration mydj --initial" --> this will create the initial migration files for the app

8. then run south migrate--> "python manage.py migrate mydj" ,this will add the tables to the database.

9. run python "manage.py runserver" to start the server.

10. go to localhost:8000

11. signup for voting app.

12. create a Poll.

13. Answer polls asked by others.