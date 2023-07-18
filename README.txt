README

Tosia: Flask Web Application
Welcome to Tosia, a Flask web application that helps pet owners manage their pets, book veterinary visits and see a history of visits.

The application uses a SQLite database to store the data and SQLAlchemy as the ORM.

Application Structure

The application consists of three main models:

* Pet: Represents the pets owned by users.
* Clinic: Represents the veterinary clinics available for visits.
* Visit: Represents a veterinary visit, related to both a pet and a clinic.

The application also consists of six main routes:

* Home ('/'): The home page.
* Add Pet ('/addpet'): A page to add a new pet.
* Confirm Delete ('/confirmdelete'): A confirmation page for deleting a pet.
* Delete Pet ('/deletepet'): A route to delete a pet.
* Book Visit ('/bookvisit'): A page to book a veterinary visit.
* Visit History ('/visithistory'): A page showing a history of veterinary visits.

How to Run

Prerequisites

Make sure you have the following installed on your system:

Python 3.7 or higher
Flask 1.1.2 or higher
Flask-SQLAlchemy 2.4.4 or higher
Requests 2.25.1 or higher

Steps

1. Clone this repository to your local machine.
2. Navigate to the repository's directory through the terminal.
3. Install the necessary dependencies with the following command:

pip install -r requirements.txt

Run the application using the following command:

python app.py

Open a web browser and navigate to http://127.0.0.1:5000/ to see the application in action.

Enjoy managing your pets with the Tosia Flask application!

Note: This application is set to run in debug mode for development purposes. For deployment, make sure to set debug=False in the app.run() function.