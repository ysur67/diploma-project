from django.contrib import admin
from apps.main.models import SiteSettings, MainSlider, IndexCategories



class MainSliderInline(admin.TabularInline):
    model = MainSlider
    extra = 0

class IndexCategoryAdmin(admin.TabularInline):
    model = IndexCategories
    extra = 0


@admin.register(SiteSettings)
class SettingsAdmin(admin.ModelAdmin):
    inlines = [MainSliderInline, IndexCategoryAdmin]
