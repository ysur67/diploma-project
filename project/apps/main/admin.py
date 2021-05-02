from django.contrib import admin

# Register your models here.
from apps.main.models import SiteSettings

@admin.register(SiteSettings)
class SettingsAdmin(admin.ModelAdmin):
    pass