from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Nutzer

class NutzerAdmin(BaseUserAdmin):
    model = Nutzer
    list_display = ('email', 'eingeloggt', 'gesperrt')
    search_fields = ('email',)
    ordering = ('email',)
    
    # Entferne alle nicht vorhandenen Felder
    list_filter = ()  # keine Filter
    filter_horizontal = ()  # keine Gruppen oder Berechtigungen

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Status', {'fields': ('eingeloggt', 'gesperrt')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

admin.site.register(Nutzer, NutzerAdmin)
