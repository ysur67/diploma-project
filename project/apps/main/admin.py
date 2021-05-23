from django.contrib import admin
from apps.main.models import SiteSettings


@admin.register(SiteSettings)
class SettingsAdmin(admin.ModelAdmin):
    pass
