from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 📡 Inyección de protocolos de rastreo
from django.contrib.sitemaps.views import sitemap
from marketapp.sitemaps import PublicacionSitemap, StaticViewSitemap

sitemaps = {
    'publicaciones': PublicacionSitemap,
    'static': StaticViewSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('marketapp.urls')),
    path('accounts/', include('allauth.urls')),
    
    # 🛰️ Ruta del Radar para Google (Sitemap)
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]

# Radar de archivos multimedia activo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
