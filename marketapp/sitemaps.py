from django.contrib.sitemaps import Sitemap
from .models import Publicacion  # Cambiado a Publicacion
from django.urls import reverse

# Mapa para las Publicaciones (Ventas, Alquileres, etc.)
class PublicacionSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        # Solo rastreamos lo que no está vendido para no engañar a Google
        return Publicacion.objects.filter(vendido=False)

    def lastmod(self, obj):
        return obj.fecha_creacion 

# Mapa para páginas estáticas
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        # Asegúrate de que 'home' es el name de tu URL principal
        return ['home'] 

    def location(self, item):
        return reverse(item)
