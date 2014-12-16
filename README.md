This README is for the Departure Times project for the Coding Challenge.
This project provides a service to get real-time departure times using 511 Real-Time Transit Departures API.
It has been implemented in Python and uses the Django framework. 
Front end has an index.html, results.html and uses JS, CSS, HTML and jquery framework to perform the ajax calls. 
It allows user to select Agency, followed by a route and or route direction and finally a stop, from the drop down menu to get the departure times. 

App deployed on google app engine at  departuretimes.appspot.com

To deploy locally:
 copy the git code
 python manage.py runserver
 http://127.0.0.1:8000/
