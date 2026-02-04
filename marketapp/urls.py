
from django.urls import path
from . import views

urlpatterns = [
    # --- NÚCLEO DEL SISTEMA ---
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'), 
    path('stats/', views.stats_global, name='stats'), 
    path('perfil/', views.perfil, name='perfil'),
    
    # --- GESTIÓN DE ANUNCIOS (SIN DUPLICADOS) ---
    path('vender/', views.vender_producto, name='vender'), # Una sola ruta limpia
    path('detalle/<int:pk>/', views.detalle_anuncio, name='detalle'),
    path('editar/<int:pk>/', views.gestionar_anuncio, name='editar_anuncio'),
    path('eliminar/<int:pk>/', views.eliminar_anuncio, name='eliminar_anuncio'),
    # Cambia 'pk' por 'anuncio_id' para que coincida con tu vista
     path('marcar-vendido/<int:anuncio_id>/', views.marcar_vendido, name='marcar_vendido'),
     path('anuncio/reactivar/<int:anuncio_id>/', views.reactivar_anuncio, name='reactivar_anuncio'),
    
    # --- PROTOCOLO DE ACCESO (LOGIN CYBERPUNK) ---
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_view, name='registro'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    
    path('backup/descargar/', views.descargar_backup, name='backup_sistema'),
    path('backup/restaurar/', views.restaurar_backup, name='restaurar_backup'), # LA NUEVA
]
