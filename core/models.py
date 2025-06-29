rom django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from simple_history.models import HistoricalRecords


class CompanyInfo(models.Model):
    """
    Informazioni aziendali globali
    """
    name = models.CharField(
        max_length=200, 
        verbose_name="Nome Azienda",
        default="giiSoftware Spa"
    )
    tagline = models.CharField(
        max_length=300, 
        blank=True,
        verbose_name="Slogan/Tagline",
        default="Sistema Gestionale Beverage & Food"
    )
    address_line_1 = models.CharField(
        max_length=200,
        verbose_name="Indirizzo (Riga 1)",
        default="Via Tione degli Abruzzi, 19"
    )
    address_line_2 = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Indirizzo (Riga 2)",
        default="00132 Roma (RM)"
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Telefono",
        default="+39 393 9657180"
    )
    email = models.EmailField(
        verbose_name="Email",
        default="danigioloso@gmail.com"
    )
    vat_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Partita IVA",
        validators=[
            RegexValidator(
                regex=r'^IT[0-9]{11}$',
                message='Formato P.IVA non valido (es: IT12345678901)'
            )
        ]
    )
    website = models.URLField(
        blank=True,
        verbose_name="Sito Web",
        default="https://www.giiholding.it"
    )
    logo = models.ImageField(
        upload_to='company/logos/',
        blank=True,
        null=True,
        verbose_name="Logo Aziendale"
    )
    
    # Configurazioni sistema
    items_per_page = models.PositiveIntegerField(
        default=25,
        verbose_name="Elementi per Pagina"
    )
    pdf_font_size = models.PositiveIntegerField(
        default=10,
        verbose_name="Dimensione Font PDF"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Informazioni Azienda"
        verbose_name_plural = "Informazioni Azienda"
    
    def __str__(self):
        return self.name
    
    def get_full_address(self):
        """Restituisce indirizzo completo"""
        if self.address_line_2:
            return f"{self.address_line_1}, {self.address_line_2}"
        return self.address_line_1
    
    def get_logo_url(self):
        """Restituisce URL logo o placeholder"""
        if self.logo:
            return self.logo.url
        return '/static/images/default-logo.png'
    
    @classmethod
    def get_company(cls):
        """Restituisce l'istanza company (singleton pattern)"""
        company, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'name': 'giiSoftware Spa',
                'tagline': 'Sistema Gestionale Beverage & Food',
                'address_line_1': 'Via Tione degli Abruzzi, 19',
                'address_line_2': '00132 Roma (RM)',
                'phone': '+39 393 9657180',
                'email': 'danigioloso@gmail.com',
                'website': 'https://www.giiholding.it',
            }
        )
        return company


class SystemSettings(models.Model):
    """
    Impostazioni di sistema globali
    """
    THEME_CHOICES = [
        ('light', 'Chiaro'),
        ('dark', 'Scuro'),
        ('auto', 'Automatico'),
    ]
    
    LANGUAGE_CHOICES = [
        ('it', 'Italiano'),
        ('en', 'English'),
    ]
    
    # Impostazioni UI
    theme = models.CharField(
        max_length=10,
        choices=THEME_CHOICES,
        default='light',
        verbose_name="Tema"
    )
    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='it',
        verbose_name="Lingua"
    )
    
    # Impostazioni sistema
    enable_email_notifications = models.BooleanField(
        default=True,
        verbose_name="Notifiche Email"
    )
    enable_audit_trail = models.BooleanField(
        default=True,
        verbose_name="Audit Trail"
    )
    session_timeout_minutes = models.PositiveIntegerField(
        default=60,
        verbose_name="Timeout Sessione (minuti)"
    )
    
    # Impostazioni backup
    enable_auto_backup = models.BooleanField(
        default=False,
        verbose_name="Backup Automatico"
    )
    backup_frequency_days = models.PositiveIntegerField(
        default=7,
        verbose_name="Frequenza Backup (giorni)"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Audit trail
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = "Impostazioni Sistema"
        verbose_name_plural = "Impostazioni Sistema"
    
    def __str__(self):
        return f"Impostazioni Sistema - {self.theme}/{self.language}"
    
    @classmethod
    def get_settings(cls):
        """Restituisce l'istanza settings (singleton pattern)"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class BaseModel(models.Model):
    """
    Modello base astratto per tutti i modelli del sistema
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Creato il"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Aggiornato il"
    )
    created_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name="Creato da"
    )
    updated_by = models.ForeignKey(
        'auth.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        verbose_name="Aggiornato da"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Attivo"
    )
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        """Override save per timestamp automatici"""
        if not self.pk:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)