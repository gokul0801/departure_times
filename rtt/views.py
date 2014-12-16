from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rtt.queries_lxml import getAgencies, getRoutes, getDirectionsForRoute, getStopsForRoute, getDepartureTimes
import json, log


def index(req):
    agencies = getAgencies()
    return render_to_response('index.html', { 'agencies' : agencies })


@csrf_exempt
def selectRoutes(req):
    if req.method == 'POST':
       routes, hasDirection = getRoutes(req.POST['agency'])
       response = dict()
       response["routes"] = []
       for route in routes:
	   response["routes"].append( {"route": route.name} )
       response["hasDirection"] = hasDirection
       log.debug(response["routes"])
       log.debug(response.get("hasDirection"))
       return HttpResponse(json.dumps(response), mimetype='application/json')
        

### View for selecting direction
@csrf_exempt
def selectDirections(req):
    if req.method == 'POST':
       routeDirectionList = getDirectionsForRoute(req.POST['agency'], req.POST['route'])
       output = []
       for direction in routeDirectionList:
	   output.append({"direction": direction.name})
       return HttpResponse(json.dumps(output), mimetype='application/json')

### View for selecting stops
@csrf_exempt
def selectStops(req):
    if req.method == 'POST':
       log.debug(req.POST)
       if 'direction' in req.POST:
	   stopList = getStopsForRoute(req.POST['agency'],
				       req.POST['route'],
	                               req.POST['direction'])
       else:
	   stopList = getStopsForRoute(req.POST['agency'],
				       req.POST['route'])
       output = []
       for stop in stopList:
	   output.append({"stop": stop.name})
       return HttpResponse(json.dumps(output), mimetype='application/json')
 

### View for displaying departure times
### Output route has the times for the selected route and stop.
### Also return data for other routes for that stop.
@csrf_exempt
def displayTimes(req):
    if req.method == 'POST':
       agency = req.POST['agency']
       selectRoute = req.POST['route']
       stop = req.POST['stop']
       selectDirection = ''
       if 'direction' in req.POST:
	 selectDirection = req.POST['direction']
       log.debug(req.POST)
       routeTimesList = getDepartureTimes(agency, stop)
       outputRoute = None
       otherRoutes = []
       for route in routeTimesList:
           log.debug(route)
       for route in routeTimesList:
	   if route.name == selectRoute:
	      outputRoute = route
	   else:
	      otherRoutes.append(route)
    
       log.debug(outputRoute)
       log.debug(otherRoutes)
       return render_to_response('results.html', {'outputRoute': outputRoute,
		                           	  'otherRoutes': otherRoutes,
						  'routeName': selectRoute,
					          'selectDirection': selectDirection,
					          'stopName': stop,
	                                          'otherRoutesLen': len(otherRoutes)})
				        
		                        
       

