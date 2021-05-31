from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from .models import Peca, DemandaDePeca, User
from django.utils.html import format_html

# Register your models here.

admin.site.register(Peca)

# class DemandaProfileAdmin(admin.ModelAdmin):
#     list_display = ['status_de_finalizacao']

#     def status_de_finalizacao(self, obj):
#         if obj.status_de_finalizacao:
#             return True
#         return False
#     status_de_finalizacao.boolean = True

@admin.register(DemandaDePeca)
class HeroAdmin(admin.ModelAdmin):
    list_display = ['status_de_finalizacao']
    list_filter = ('status_de_finalizacao',)

    def status_de_finalizacao(self, obj):
        return obj.status_de_finalizacao == True

    status_de_finalizacao.boolean = True




class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'is_administrador', 'is_anunciante', 'full_name']

    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


admin.site.register(User, UserProfileAdmin)
# admin.site.register(DemandaDePeca, DemandaProfileAdmin)
admin.site.site_header = 'Finxi | Django MVC'