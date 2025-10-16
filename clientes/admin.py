from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'produto_favorito', 'criado_em')
    search_fields = ('nome', 'email')
    list_filter = ('criado_em',)
