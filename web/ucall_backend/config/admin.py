from config.models import Config, AmiConfig, StompConfig, GeneralConfig
from django.contrib import admin

class ConfigAdmin(admin.ModelAdmin):
    pass

class AmiConfigAdmin(admin.ModelAdmin):
    pass

class StompConfigAdmin(admin.ModelAdmin):
    pass

class GeneralConfigAdmin(admin.ModelAdmin):
    pass

admin.site.register(Config, ConfigAdmin)
#admin.site.register(AmiConfig, AmiConfigAdmin)
#admin.site.register(StompConfig, StompConfigAdmin)
#admin.site.register(GeneralConfig, GeneralConfigAdmin)
