# Meal-Spot
#### Online Restaurant System 
*Built using the Django framework*

## Requirements
You need to have the latest version of python installed (3.7+) and pip as well.
Google Chrome or Chromium is recommended if you want to try the voice order feature.
An internet connection is needed for jQuery, bootstrap, and our Google Maps API to work.
You may also want to use a python virtual environment to run this app to avoid dependency issues.

## Starting and running your project
1. Clone this repository
2. In the /src directory add a file called db.sqlite3 to have your database initialized, we are using sqlite3
3. Now in your terminal, move to the src directory, type ls or dir (depending on your OS) and if manage.py shows up in your
result, you are good to go.
4. Type the following commands to setup your project:

	 To install Django if you haven't:
	
		pip install Django 

	
	To see your arguments for manage.py:
	
		python manage.py
	
	To setup your database:
	
		python manage.py migrate
		
	To setup your superuser/administrator account:
	
		python manage.py createsuperuser
5. To run the app, type;

		python manage.py runserver
You will need to type on your browser url bar to access our site:

	localhost:8000

You are free to sign in as a superuser that you created before. You will be the site administrator.
You could also sign up as any account you wish. 

In addition the label "Meal Spot" in your top left corner of your navigation bar will be a link to your home page, your homepage is different for each usertype.

## Bugs
- There is possibly a bug regarding usernames where if you sign up and you get an error then you can't use that username again, (it still needs to be tested to what extent this bug exists as it has been fixed for customer and manager usertypes). 
