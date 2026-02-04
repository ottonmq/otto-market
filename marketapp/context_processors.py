from django.db.models import Sum
from .models import Publicacion, User

def contadores_globales(request):
    # 1. Calculamos la suma real de todas las vistas de los anuncios del usuario
    if request.user.is_authenticated:
        vistas_reales = Publicacion.objects.filter(vendedor=request.user).aggregate(Sum('vistas'))['vistas__sum'] or 0
    else:
        vistas_reales = 0

    # 2. Retornamos el diccionario con los nombres exactos que usas en el HTML
    return {
        # Para el HUD Estático
        'online': User.objects.count(), 
        'vistas': vistas_reales,
        
        # Para el Dashboard (Estructura de objeto 'stats')
        'stats': {
            'vistas_totales': vistas_reales,
            'total_items': Publicacion.objects.filter(vendido=False).count(),
        },
        
        'trafico_red': 1240,
    }
