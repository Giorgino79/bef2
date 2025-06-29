
from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import CompanyInfo, SystemSettings


@admin.register(CompanyInfo)
class CompanyInfoAdmin(SimpleHistoryAdmin):
    """Admin per informazioni aziendali"""
    
    list_display = [
        'name', 'email', 'phone', 'vat_number', 
        'updated_at'
    ]
    
    fieldsets = (
        ('Informazioni Base', {
            'fields': ('name', 'tagline', 'email', 'phone')
        }),
        ('Indirizzo', {
            'fields': ('address_line_1', 'address_line_2')
        }),
        ('Dati Fiscali', {
            'fields': ('vat_number', 'website')
        }),
        ('Media', {
            'fields': ('logo',)
        }),
        ('Configurazioni', {
            'fields': ('items_per_page', 'pdf_font_size'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_delete_permission(self, request, obj=None):
        """Impedisce eliminazione delle info aziendali"""
        return False


@admin.register(SystemSettings)
class SystemSettingsAdmin(SimpleHistoryAdmin):
    """Admin per impostazioni sistema"""
    
    list_display = [
        'theme', 'language', 'enable_email_notifications',
        'session_timeout_minutes', 'updated_at'
    ]
    
    fieldsets = (
        ('Interfaccia Utente', {
            'fields': ('theme', 'language')
        }),
        ('Notifiche e Sicurezza', {
            'fields': (
                'enable_email_notifications', 
                'enable_audit_trail',
                'session_timeout_minutes'
            )
        }),
        ('Backup', {
            'fields': ('enable_auto_backup', 'backup_frequency_days'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def has_delete_permission(self, request, obj=None):
        """Impedisce eliminazione delle impostazioni"""
        return False