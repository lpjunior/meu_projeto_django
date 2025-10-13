from django.contrib import admin
from app.models import Produto

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'criado_em')
    search_fields = ('nome',)
    list_filter = ('criado_em',)