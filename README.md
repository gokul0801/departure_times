This README is for the Departure Times project for the Coding Challenge.
This project provides a service to get real-time departure times using 511 Real-Time Transit Departures API.
It has been implemented in Python and uses the Django framework. 
Front end has an index.html, results.html and uses JS, CSS, HTML and jquery framework to perform the ajax calls. 
It allows user to select Agency, followed by a route and or route direction and finally a stop, from the drop down menu to get the departure times. 

App deployed on google app engine at  http://departuretimes.appspot.com

Code is organized as follows:
 rtt directory has the app specific code - 
    urls.py -   list of urls for 'rtt' app 
    views.py -  Views for  selecting agencies, routes, stops and displaying departure times.
    queries_lxml.py -  Modules called from views for getting data  from 511 webservice and parsing xml results.
    templates  - directory  for front end html files
    static directory for  javascript & css files.    main.js file has the jquery code.
    log.py  
 DepartureTimes - project directory containing django settings.py
 app.yaml - settings file for deploying app to Google app engine.
 manage.py
