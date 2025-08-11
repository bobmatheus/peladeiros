# main/context_processors.py
from django.conf import settings

def settings_extras(request):
    return {
        'API_BASE_URL': getattr(settings, 'API_BASE_URL', ''),
    }