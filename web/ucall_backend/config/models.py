from django.db import models

STOMP = 'stomp'
AMI = 'ami'
GENERAL = 'general'

KIND_CHOICES = (
    (STOMP, STOMP),
    (AMI, AMI),
    (GENERAL, GENERAL),
)


class Config(models.Model):
    CONFIG_SECTIONS = (
        (u'general', u'general'),
        (u'stomp', u'stomp'),
        (u'ami', u'ami'),
        (u'voip', u'voip'),
        (u'app', u'app'),
    )

    section = models.CharField(max_length=255, choices=CONFIG_SECTIONS)
    key = models.CharField(max_length=255)
#    kind = models.CharField(max_length=255, editable=False, choices=KIND_CHOICES)
    value = models.CharField(max_length=255)

    def __unicode__(self):
        return self.key

#    def save(self, *args, **kwargs):
#        if not self.kind:
#            self.kind = self.exact_type

#        super(Config,self).save(*args, **kwargs)

class StompConfig(Config):

    exact_type = STOMP

    ctrl_channel = models.CharField(max_length=255)
    agent_channel_prefix = models.CharField(max_length=255)
    stomp_url = models.CharField(max_length=255)
    ws_url = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255) 

class AmiConfig(Config):

    exact_type = AMI

    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255) 

class GeneralConfig(Config):

    exact_type = GENERAL

    name = models.CharField(max_length=255)
    