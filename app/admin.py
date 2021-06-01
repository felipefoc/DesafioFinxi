from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import Peca, DemandaDePeca, Usuario
from django.utils.html import format_html

# Register your models here.

admin.site.register(Peca)

@admin.register(DemandaDePeca)
class DemandaProfileAdmin(admin.ModelAdmin):
    list_display = ['status_de_finalizacao']

    def status_de_finalizacao(self, obj):
        if obj.status_de_finalizacao:
            return True
        return False
    status_de_finalizacao.boolean = True

@admin.register(Usuario)
class UsuarioProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'administrador', 'anunciante', 'full_name']

    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'



admin.site.site_header = 'Finxi | Django MVC'