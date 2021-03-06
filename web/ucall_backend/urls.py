import os
import sys

from django.conf.urls.defaults import patterns, include, url
from ucall.rpc import Router
from django.contrib import admin

PROJECT_ROOT = os.path.dirname(__file__)
FORMUNCULOUS_STATIC_MEDIA_PATH = os.path.join(PROJECT_ROOT, "vendors", "formunculous", "formunculous", "media", "formunculous")

admin.autodiscover()
router = Router()

urlpatterns = patterns('',
    url(r'^profile-save/', 'ucall.views.profile_save'),
    url(r'^router/$', router, name='router'),
    url(r'^router/api/$', router.api, name='api'),
    url(r'^$', 'ucall_ui.views.main', name="root"),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),
    url(r'^admin/', include(admin.site.urls), name="admin"),
    url(r'^profile/', 'ucall.views.main', name="profile"),
    url(r'^config/', include('config.urls')),

    # include formunculous urls
    (r'^func/', include('formunculous.urls')),
    # formunculous static urls

    (r'formunculous/(?P<path>.*)$', 'django.views.static.serve', {'document_root': FORMUNCULOUS_STATIC_MEDIA_PATH, 'show_indexes': False}),    
)
