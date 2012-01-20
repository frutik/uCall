from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^stomp/', 'config.views.config_stomp', name="config_stomp"),
    url(r'^current_user/', 'config.views.config_current_user', name="config_current_user"),
    url(r'^channel_event_schema/', 'config.views.config_channel_event_schema', name="config_channel_event_schema"),
    url(r'^urls/', 'config.views.config_urls', name="config_urls"),
    url(r'^app/', 'config.views.config_app', name="config_app"),
    url(r'^voip/', 'config.views.config_voip', name="config_voip"),
)
