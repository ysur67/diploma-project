from apps.main.models import SiteSettings

def load_settings(request):
    return {'site_settings': SiteSettings.objects.first()}
