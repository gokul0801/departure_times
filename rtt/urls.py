from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('rtt.views',
   url('ajax/getRoutes/', 'selectRoutes'),
   url('ajax/getDirections/', 'selectDirections'),
   url('ajax/getStops/', 'selectStops'),
   url('displayTimes', 'displayTimes'),
   url('refreshResults', 'refreshResults'),
   url(r'^$', 'index'))
   

