from django.contrib import admin
from django.utils.html import format_html
from .models import Perfil, Categoria, Publicacion, Imagen

# Personalización del Header con estilo Tech
admin.site.site_header = "OTTO-MARKET // CENTRAL_CORE"
admin.site.index_title = "SISTEMA DE GESTIÓN DE ACTIVOS"
admin.site.site_title = "OTTO-MARKET ADMIN"

# --- PROTOCOLO DE GALERÍA (INLINE) ---
class ImagenInline(admin.TabularInline):
    model = Imagen
    extra = 1  # Permite subir una foto extra por defecto
    fields = ('imagen',) # Ahora coincide con el nombre en models.py

@admin.register(Publicacion)
class PublicacionAdmin(admin.ModelAdmin):
    # Visualización principal con ID de neón
    list_display = ('id_tag', 'titulo', 'categoria', 'precio', 'vendedor', 'vendido')
    list_editable = ('vendido',) 
    list_filter = ('categoria', 'tipo_negocio', 'vendido')
    search_fields = ('titulo', 'marca', 'modelo')
    
    # Reactivamos la galería dentro de la publicación
    inlines = [ImagenInline]
    
    # Estética Tech para los IDs
    def id_tag(self, obj):
        return format_html('<code style="color: #00f3ff; font-weight: bold; background: #000; padding: 2px 5px; border-radius: 3px;">[UNIT-{}]</code>', obj.id)
    id_tag.short_description = 'SERIAL_ID'

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'nombre', 'telefono', 'fecha_unido')
    search_fields = ('usuario__username', 'telefono')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

# Registro independiente de imágenes para gestión masiva
@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    list_display = ('id', 'publicacion', 'imagen_preview')
    
    def imagen_preview(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 50px; height: auto; border: 1px solid #00f3ff;" />', obj.imagen.url)
        return "SIN_DATA"
    imagen_preview.short_description = 'PREVIEW'
