from django.conf import settings
from django.utils import timezone
from .models import CompanyInfo, SystemSettings


def company_info(request):
    """
    Rende disponibili le informazioni aziendali in tutti i template
    """
    try:
        company = CompanyInfo.get_company()
        return {
            'company_info': company,
            'company': company,  # Alias per compatibilità
        }
    except Exception:
        return {
            'company_info': None,
            'company': None,
        }


def global_settings(request):
    """
    Rende disponibili impostazioni globali e informazioni di sistema
    """
    try:
        system_settings = SystemSettings.get_settings()
    except Exception:
        system_settings = None
    
    return {
        'system_settings': system_settings,
        'current_year': timezone.now().year,
        'debug_mode': settings.DEBUG,
        'app_name': 'BEF2PRO',
        'app_version': '2.0.0',
        'company_short_name': 'giiSoftware',
    }


def user_preferences(request):
    """
    Preferenze utente e informazioni sessione
    """
    if request.user.is_authenticated:
        return {
            'user_full_name': request.user.get_full_name() or request.user.username,
            'user_short_name': request.user.first_name or request.user.username[:10],
            'is_staff_user': request.user.is_staff,
            'is_superuser': request.user.is_superuser,
        }
    
    return {
        'user_full_name': '',
        'user_short_name': '',
        'is_staff_user': False,
        'is_superuser': False,
    }