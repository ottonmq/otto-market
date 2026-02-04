from django.contrib import admin
from django.utils.html import format_html
from .models import Perfil, Categoria, Publicacion, Imagen

admin.site.site_header = "OTTO-MARKET // CENTRAL_CORE"

class ImagenInline(admin.TabularInline):
    model = Imagen
    extra = 1

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    # 'vendido' es el interruptor funcional aquí
    list_display = ('id_tag', 'titulo', 'categoria', 'precio', 'vendedor', 'vendido')
    list_editable = ('vendido',) 
    list_filter = ('categoria', 'tipo_negocio', 'vendido')
    search_fields = ('titulo', 'marca', 'modelo')
    inlines = [ImagenInline]
    
    def id_tag(self, obj):
        return format_html('<code style="color: #00f3ff; font-weight: bold;">[UNIT-{}]</code>', obj.id)
    id_tag.short_description = 'SERIAL_ID'

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefono', 'fecha_unido')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'id')
