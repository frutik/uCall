from django.db import models

class Org(models.Model):
    title = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.title

class Contact(models.Model):
    title = models.CharField(max_length=255)
    org = models.ForeignKey(Org)
    phone = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.title

