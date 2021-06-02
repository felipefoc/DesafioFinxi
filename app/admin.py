from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import Peca, DemandaDePeca, Usuario
from django.utils.html import format_html

# Register your models here.

@admin.register(Peca)
class PecaProfileAdmin(admin.ModelAdmin):
    list_display = ['modelo', 'descricao']

@admin.register(DemandaDePeca)
class DemandaProfileAdmin(admin.ModelAdmin):
    list_display = ['anunciante', 'informacoes_de_contato', 'finalizado']

    def finalizado(self, obj):
        if obj.status_de_finalizacao == True:
            return True
        return False
    finalizado.boolean = True

@admin.register(Usuario)
class UsuarioProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'administrador', 'anunciante', 'full_name']
    model = UserAdmin
    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

admin.site.site_header = 'Finxi | Django MVC'