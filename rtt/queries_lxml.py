import urllib, urllib2
import log
import sys
import lxml
from lxml import etree

BASE_URL = 'http://services.my511.org/Transit2.0/'
SECURITY_TOKEN = '4272b807-452a-406b-b034-d2b471318fea'
sessionCache = {}
routes_dict_cache = {}

def getXml(requestURL):
    try:
        return sessionCache[requestURL]
    except KeyError:
        xml = urllib2.urlopen(requestURL)
        sessionCache[requestURL] = xml
        return xml

#Classes for Agency, Route, RouteDirection and Stop
class Agency:
  def __init__(self, name, hasDirection):
      self.name = name
      self.hasDirection = hasDirection
      self.routes = []

  def addRoute(self, route):
      self.routes.append(route)

  def __str__(self):
      return "<Agency Name:%s, hasDirection:%s>" % (self.name, self.hasDirection)


class Route:
  def __init__(self, name, code):
      self.name = name
      self.code = code
      self.routeDirectionList = []
      ### stopList used for agencies that dont have route direction
      ### For other agencies, stoplist is stored in the route direction list
      self.stopList = []     

  def addRouteDirection(self, routeDirection):
      self.routeDirectionList.append(routeDirection)

  def addStop(self, stop):
      self.stopList.append(stop)

  def __str__(self):
      result = "<Route Name:%s, Code:%s>\n" % (self.name, self.code)
      if self.routeDirectionList != []:
	 for routeDir in self.routeDirectionList:
	     result += str(routeDir) + '\n'
      else:
	 for stop in self.stopList:
	     result += str(stop) + '\n'
      return result

  def hasDirectionList(self):
      if self.routeDirectionList != []:
	 return True
      else:
	 return False


##RouteDirection has list of stops to store data for stops
class RouteDirection:
  def __init__(self, name, code):
      self.name = name
      self.code = code
      self.stopList = []   

  def __str__(self):
      result = "<RouteDirection Name:%s, Code:%s>\n" % (self.name, self.code)
      for stop in self.stopList:
	  result += str(stop) + '\n'
      return result


  def addStop(self, stop):
      self.stopList.append(stop)



class Stop:
   def __init__(self, name, code):
       self.name = name
       self.code = code
       self.departureTimeList = []

   def __str__(self):
       result = "<Stop Name:%s, Code:%s>" % (self.name, self.code)
       if len(self.departureTimeList) != 0:
	  result += '\nDepartureTimes: '
	  num = len(self.departureTimeList)
	  for i in range(0, num-1):
	      result += self.departureTimeList[i] + ', '    
          result += self.departureTimeList[num-1] + ' mins'
       else:
	  result += '\nNo data available..'
       return result

   ### Return list of departure times for this stop
   def getDepartureList(self):
       result = ''
       if len(self.departureTimeList) != 0:
	  num = len(self.departureTimeList)
	  for i in range(0, num-1):
	      result += self.departureTimeList[i] + ', '    
          result += self.departureTimeList[num-1] + ' mins'
       else:
	  result += 'No data available..'
       return result

   def addDepartureTime(self, time):
       self.departureTimeList.append(time)



def getAgencies():
  try:
    url = BASE_URL + 'GetAgencies.aspx?token=%s' % SECURITY_TOKEN
    print url
    xml = getXml(url)
    dom = etree.parse(xml)
    agencies = []
    for agency in dom.xpath('//RTT/AgencyList/Agency'):
	name = agency.xpath('@Name')[0]
	hasDirection = agency.xpath('@HasDirection')[0]
	agency = Agency(name, hasDirection)
	print agency
	agencies.append(agency)
    return agencies
  except:
    raise Exception("Error getting Transit Agency list: %s %s" % (sys.exc_type, sys.exc_value))



def getRoutes(agency):
  try:
    if routes_dict_cache.has_key(agency):
       route = routes_dict_cache[agency][0]
       if route.routeDirectionList == []:
	  hasDirection = 'False'
       else:
	  hasDirection = 'True'      
       return routes_dict_cache[agency], hasDirection
    params = urllib.urlencode({'agencyName': agency})
    url = BASE_URL + 'GetRoutesForAgency.aspx?'+ params + '&token=%s' % SECURITY_TOKEN
    print url
    log.debug(url)
    xml = getXml(url)
    dom = etree.parse(xml)
    routes = []
    hasDirection = dom.xpath('//RTT/AgencyList/Agency/@HasDirection')[0]
    print hasDirection
    for route in dom.xpath('//RTT/AgencyList/Agency/RouteList/Route'):
	routeName = route.xpath('@Name')[0]
	routeCode = route.xpath('@Code')[0]
	routeObj = Route(routeName, routeCode)
        if route.xpath('RouteDirectionList') != []:
	   for routeDirection in route.xpath('RouteDirectionList/RouteDirection'):
               routeDirectionName = routeDirection.xpath('@Name')[0]
	       routeDirectionCode = routeDirection.xpath('@Code')[0]
	       routeDirectionObj = RouteDirection(routeDirectionName, routeDirectionCode)
	       routeObj.addRouteDirection(routeDirectionObj)
        print routeObj	
	routes.append(routeObj)
    routes_dict_cache[agency] = routes
    return routes, hasDirection
  except:
    raise Exception("Error getting routes for Agency %s" % agency + ":%s %s" % (sys.exc_type, str(sys.exc_value)))



def getDirectionsForRoute(agency, routename):
  try:
    for route in routes_dict_cache[agency]:
	if route.name == routename:
	   return route.routeDirectionList
  except:
     raise Exception("Error getting directions for Agency %s, Route %s" % (agency, routename))


def getStopsForRoute(agency, routeName, routeDirectionName=None):
  try:
    routeCode = ''
    routeDirectionCode = ''
    log.debug(routeDirectionName)
    for route in routes_dict_cache[agency]:
	if route.name == routeName:
	   routeCode = route.code
	   if routeDirectionName is not None:
	      for direction in route.routeDirectionList:
	          if direction.name == routeDirectionName:
	             routeDirectionCode = direction.code
	
    if routeDirectionName is None:
       routeIDF = agency + '~' + routeCode
       params = urllib.urlencode({'routeIDF': routeIDF})
       url = BASE_URL + 'GetStopsForRoute.aspx?' + params + '&token=%s' % SECURITY_TOKEN
       path = '//RTT/AgencyList/Agency/RouteList/Route/StopList/Stop'
    else:
       routeIDF = agency + '~' + routeCode + '~' + routeDirectionCode
       params = urllib.urlencode({'routeIDF': routeIDF})
       url = BASE_URL + 'GetStopsForRoute.aspx?' + params + '&token=%s' % SECURITY_TOKEN
       path = '//RTT/AgencyList/Agency/RouteList/Route/RouteDirectionList/RouteDirection/StopList/Stop'
    xml = getXml(url)
    dom = etree.parse(xml)
    stops = []
    for stop in dom.xpath(path):
	stopName = stop.xpath('@name')[0]
	stopCode = stop.xpath('@StopCode')[0]
	stopObj = Stop(stopName, stopCode)
	stops.append(stopObj)
	print stopName
    return stops
  except:
    raise Exception("Error getting stops for Agency %s, Route %s" % (agency, routeName))
    
  


def getDepartureTimes(agency, stopName):
  try:
    params = urllib.urlencode({'agencyName': agency, 'stopName': stopName})
    url = BASE_URL + 'GetNextDeparturesByStopName.aspx?' + params + '&token=%s' % SECURITY_TOKEN
    print url
    xml = urllib2.urlopen(url)
    dom = etree.parse(xml)
    routeTimes = []
    hasDirection = dom.xpath('//RTT/AgencyList/Agency/@HasDirection')[0]
    for route in dom.xpath('//RTT/AgencyList/Agency/RouteList/Route'):
        routeName = route.xpath('@Name')[0]
	routeCode = route.xpath('@Code')[0]
	routeObj = Route(routeName, routeCode)
        if hasDirection == 'True':
	   for routeDirection in route.xpath('RouteDirectionList/RouteDirection'):
	       routeDirectionName = routeDirection.xpath('@Name')[0]
	       routeDirectionCode = routeDirection.xpath('@Code')[0]
	       routeDirectionObj = RouteDirection(routeDirectionName, routeDirectionCode)
	       routeObj.addRouteDirection(routeDirectionObj)
               for stop in routeDirection.xpath('StopList/Stop'):
	           stopName = stop.xpath('@name')[0]
		   stopCode = stop.xpath('@StopCode')[0]
		   stopObj = Stop(stopName, stopCode)
		   routeDirectionObj.addStop(stopObj)    
                   if len(stop.xpath('DepartureTimeList/DepartureTime')) != 0:
	              for departureTime in stop.xpath('DepartureTimeList/DepartureTime'):
	                  stopObj.addDepartureTime(departureTime.text)
        else: 
	   for stop in route.xpath('StopList/Stop'):
	       stopName = stop.xpath('@name')[0]
	       stopCode = stop.xpath('@StopCode')[0]
	       stopObj = Stop(stopName, stopCode)
	       routeObj.addStop(stopObj)
               if len(stop.xpath('DepartureTimeList/DepartureTime')) != 0:
	          for departureTime in stop.xpath('DepartureTimeList/DepartureTime'):
	              stopObj.addDepartureTime(departureTime.text)
	routeTimes.append(routeObj)
	print routeObj
    return routeTimes
  except:
    raise Exception("Error getting departure times for Agency %s, Stop %s" % (agency, stopName))      


if __name__ == '__main__':
   getAgencies()
   getRoutes('BART') 
   getStopsForRoute('BART', 'Fremont')
   getDepartureTimes('BART', 'Fremont')

    
