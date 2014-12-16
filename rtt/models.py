from django.db import models

# Create your models here.

class Agency(models.Model):
    name = models.CharField(max_length=30, unique=True)
    
    def __unicode__(self):
        return '<%s>' % self.name

class Route(models.Model):
    name = models.CharField(max_length=30)
    agency = models.ForeignKey(Agency)
    code = models.IntegerField()

    def __unicode__(self):
        return '<Route:%s, Agency:%s, Code:%s' % (self.name, self.agency.name, self.code)


class Stop(models.Model):
    name = models.CharField(max_length=50)
    route = models.ForeignKey(Route)
    code = models.IntegerField()

    def __unicode__(self):
        return '<Stop:%s, StopCode:%s' % (self.name, self.code)


