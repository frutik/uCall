from models import *
from django.contrib import admin

class OrgAdmin(admin.ModelAdmin):
    pass

admin.site.register(Org, OrgAdmin)

class ContactAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contact, ContactAdmin)

