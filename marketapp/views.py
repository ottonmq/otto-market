from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.utils import timezone
from datetime import timedelta

from .models import Publicacion, Categoria, Imagen ,Perfil
from .forms import PublicacionForm 
from .forms import PerfilForm

# --- 1. ACCESO Y SEGURIDAD ---
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

# --- 2. NAVEGACIÓN PÚBLICA ---

from django.db.models import Avg, Count, Q

def home(request):
    # 1. Tu lógica de red intacta
    nodos_activos, trafico_total = obtener_conteo_red()
    query = request.GET.get('q', '').strip()
    categorias = Categoria.objects.all()

    # 2. FILTRADO + CÁLCULO DE ESTRELLAS (Aquí está la magia)
    # Usamos annotate para que cada anuncio traiga su propio promedio y total
    anuncios = Publicacion.objects.filter(vendido=False).annotate(
        promedio_estrellas=Avg('resenas__puntuacion'),
        total_resenas=Count('resenas')
    )

    if query:
        anuncios = anuncios.filter(
            Q(titulo__icontains=query) | 
            Q(marca__icontains=query) | 
            Q(categoria__nombre__icontains=query)
        ).distinct()

    # 3. REDONDEO (Para que no salga 4.3333333)
    # Esto prepara los datos antes de mandarlos al HTML
    for a in anuncios:
        a.promedio_estrellas = round(a.promedio_estrellas, 1) if a.promedio_estrellas else 0.0

    return render(request, 'home.html', {
        'anuncios': anuncios.order_by('-fecha_creacion'),
        'categorias': categorias,
        'query': query,
        'online': nodos_activos if nodos_activos > 0 else 1,
        'vistas': trafico_total
    })


def detalle_anuncio(request, pk):
    # Traemos el anuncio (mantenemos tu nombre de variable 'anuncio')
    anuncio = get_object_or_404(Publicacion, pk=pk)
    
    # Contador de vistas (tu lógica original)
    anuncio.vistas = (anuncio.vistas or 0) + 1
    anuncio.save()
    
    # --- AGREGAMOS EL CÁLCULO DE ESTRELLAS ---
    resenas = anuncio.resenas.all()
    total = resenas.count()
    promedio_data = resenas.aggregate(Avg('puntuacion'))['puntuacion__avg']
    promedio = round(promedio_data, 1) if promedio_data else 0.0
    
    # Pasamos todo al HTML
    return render(request, 'detalle.html', {
        'anuncio': anuncio, 
        'galeria': anuncio.fotos.all(),
        'promedio': promedio,
        'total': total
    })

    

# --- 3. ESTADÍSTICAS (OTTO-MARKET) ---
def stats_global(request):
    total_db = Publicacion.objects.count()
    
    # CONTADOR ONLINE REAL (Últimos 5 min)
    hace_5_min = timezone.now() - timedelta(minutes=5)
    online_real = User.objects.filter(last_login__gte=hace_5_min).count()
    
    total_vistas = Publicacion.objects.aggregate(total=Sum('vistas'))['total'] or 0
    categorias_reales = Categoria.objects.annotate(num=Count('publicacion'))

    context = {
        'total': total_db,
        'activos': online_real, # Ahora sí son personas
        'vistas': total_vistas,
        'categorias': categorias_reales,
    }
    return render(request, 'stats.html', context)

@login_required
def dashboard(request):
    mis_pubs = Publicacion.objects.filter(vendedor=request.user)
    
    stats = {
        'unidades': mis_pubs.count(),
        'vendidos': mis_pubs.filter(vendido=True).count(),
        'ingresos': mis_pubs.filter(vendido=True).aggregate(Sum('precio'))['precio__sum'] or 0,
        'vistas_totales': mis_pubs.aggregate(Sum('vistas'))['vistas__sum'] or 0,
        'recientes': mis_pubs.order_by('-fecha_creacion')[:3],
        'operadores_sistema': User.objects.count() 
    }
    return render(request, 'dashboard.html', {'stats': stats})

# --- 4. GESTIÓN (TUS NOMBRES ORIGINALES) ---
@login_required
def vender_producto(request): # REGRESO AL NOMBRE QUE TIENES EN URLS
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES)
        if form.is_valid():
            nuevo = form.save(commit=False)
            nuevo.vendedor = request.user
            nuevo.save()
            messages.success(request, "UNIDAD_REGISTRADA")
            return redirect('perfil')
    else:
        form = PublicacionForm()
    return render(request, 'vender_hardware.html', {'form': form})

@login_required
def gestionar_anuncio(request, pk=None): # PARA EDITAR
    anuncio = get_object_or_404(Publicacion, pk=pk, vendedor=request.user)
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=anuncio)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = PublicacionForm(instance=anuncio)
    return render(request, 'vender_hardware.html', {'form': form, 'editando': True})

@login_required
def perfil(request):
    return render(request, 'perfil.html', {'mis_anuncios': Publicacion.objects.filter(vendedor=request.user).order_by('-fecha_creacion')})

@login_required
def eliminar_anuncio(request, pk):
    get_object_or_404(Publicacion, pk=pk, vendedor=request.user).delete()
    return redirect('perfil')

from django.views.decorators.http import require_POST
# Busca tu función marcar_vendido y cámbiala por esta:
@login_required
def marcar_vendido(request, anuncio_id):
    # Buscamos el anuncio que sea del usuario logueado
    anuncio = get_object_or_404(Publicacion, id=anuncio_id, vendedor=request.user)
    
    # 1. Lo marcamos como vendido (Esto lo quita del Home automáticamente)
    anuncio.vendido = True
    anuncio.save()
    
    # 2. Opcional: Si quieres que devuelva un OK para el JavaScript:
    from django.http import JsonResponse
    return JsonResponse({'status': 'ok', 'message': 'Vendido correctamente'})




def obtener_conteo_red():
    # 1. Calculamos operadores (logueados hace menos de 10 min)
    limite = timezone.now() - timedelta(minutes=10)
    online = User.objects.filter(last_login__gte=limite).count()
    # 2. Sumamos las vistas de todos los anuncios
    total_vistas = Publicacion.objects.aggregate(total=Sum('vistas'))['total'] or 0
    return online, total_vistas
    
    

@login_required
def editar_perfil(request):
    # El modelo usa 'usuario', no 'user'. Ojo ahí.
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    
    if request.method == 'POST':
        # Asegurate de que PerfilForm esté importado arriba
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "PERFIL_ACTUALIZADO")
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)
    
    return render(request, 'editar_perfil.html', {'form': form})



def reactivar_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Publicacion, id=anuncio_id)
    anuncio.vendido = False
    anuncio.save()
    return redirect('perfil')


from django.core.management import call_command
from django.http import HttpResponse
from io import StringIO
from django.contrib import messages
from django.shortcuts import redirect

# LA QUE YA TENEMOS PARA BAJAR EL ARCHIVO
def descargar_backup(request):
    output = StringIO()
    call_command('dumpdata', indent=2, stdout=output)
    response = HttpResponse(output.getvalue(), content_type="application/json")
    response['Content-Disposition'] = 'attachment; filename="backup_datos_otto.json"'
    return response

# LA NUEVA PARA SUBIR EL ARCHIVO (RESTAURAR)
def restaurar_backup(request):
    if request.method == 'POST' and request.FILES.get('backup_file'):
        backup_file = request.FILES['backup_file']
        # Guardamos el archivo temporalmente para procesarlo
        with open('temp_backup.json', 'wb+') as destination:
            for chunk in backup_file.chunks():
                destination.write(chunk)
        
        try:
            call_command('loaddata', 'temp_backup.json')
            messages.success(request, "NÚCLEO REESTABLECIDO: DATOS CARGADOS [✅]")
        except Exception as e:
            messages.error(request, f"ERROR EN CARGA: {e}")
            
    return redirect('dashboard') # O a la página que quieras







from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Publicacion
import json





def pagina_bot(request):
    # Sin prefijos, directo al grano
    return render(request, 'bot_consulta.html')


from django.shortcuts import render, get_object_or_404
from django.db.models import Avg  # <--- IMPORTACIÓN VITAL 📡
from .models import Publicacion, Resena

from django.db.models import Avg

def ver_opiniones(request, pk):
    # Usamos tu modelo Publicacion
    publicacion = get_object_or_404(Publicacion, pk=pk)
    
    # GUARDAR O ACTUALIZAR (Gracias al unique_together que pusiste)
    if request.method == "POST":
        puntos = request.POST.get('puntuacion', 5)
        texto = request.POST.get('comentario', '')
        
        if texto:
            # Usamos tus campos exactos: publicacion, autor, puntuacion, comentario
            Resena.objects.update_or_create(
                publicacion=publicacion, 
                autor=request.user,
                defaults={
                    'puntuacion': int(puntos), 
                    'comentario': texto
                }
            )
            return redirect('ver_opiniones', pk=pk)

    # CÁLCULOS REALES PARA LAS BARRAS AZULES
    resenas = publicacion.resenas.all()
    total = resenas.count()
    promedio_data = resenas.aggregate(Avg('puntuacion'))['puntuacion__avg']
    promedio = round(promedio_data, 1) if promedio_data else 0.0

    # Porcentajes reales para el ancho de las barras
    def get_pct(n):
        if total == 0: return 0
        return (resenas.filter(puntuacion=n).count() / total) * 100

    context = {
        'publicacion': publicacion,
        'resenas': resenas,
        'promedio': promedio,
        'total': total,
        'b5': get_pct(5), 'b4': get_pct(4), 'b3': get_pct(3), 
        'b2': get_pct(2), 'b1': get_pct(1),
    }
    return render(request, 'opiniones.html', context)



@csrf_exempt
def bot_consulta(request):
    if request.method == 'POST':
        try:
            import requests
            import os # Asegúrate de tener import os arriba

            data = json.loads(request.body)
            # Normalizamos la entrada de texto
            texto = data.get('texto', '').strip()
            
            if not texto:
                return JsonResponse({'respuesta': "🤖 [SISTEMA]: Esperando comando..."})

            # --- NIVEL 1: ESCÁNER DE SUMINISTROS (Otto-Market Local) ---
            productos = Publicacion.objects.filter(
                Q(titulo__icontains=texto) | 
                Q(marca__icontains=texto) |
                Q(categoria__nombre__icontains=texto),
                vendido=False
            )[:3]

            if productos:
                res = "⚡ **OTTO-MARKET // SUMINISTROS** ⚡<br>"
                for p in productos:
                    if p.foto:
                        res += f'<img src="{p.foto.url}" style="width:100%; border-radius:15px; border:1px solid #00f3ff; margin:10px 0;">'
                    res += f"📦 **{p.titulo.upper()}**<br>💰 PRECIO: ${p.precio}<br>"
                return JsonResponse({'respuesta': res})

            # --- NIVEL 2: PROTOCOLO SHADOW (NUEVA CONEXIÓN AIRIA) ---
            # ACTUALIZA ESTA URL con la que te dio el botón 'Integrate' de tu nuevo agente
            url_airia = "https://api.airia.ai/v1/agent/TU_NUEVO_ID_AQUÍ/chat"
            
            headers = {
                "Authorization": f"Bearer {os.getenv('AIRIA_API_KEY')}",
                "Content-Type": "application/json"
            }
            
            # Airia v2 espera 'message', no 'prompt'
            payload = {
                "message": texto,
                "stream": False
            }

            response = requests.post(url_airia, json=payload, headers=headers, timeout=15)

            if response.status_code == 200:
                # Extraemos 'output', que es donde Shadow envía su respuesta
                shadow_res = response.json().get('output', 'Shadow está procesando en las sombras...')
                return JsonResponse({'respuesta': f"👤 **SHADOW**: {shadow_res}"})
            else:
                return JsonResponse({'respuesta': f"⚠️ [ERROR]: Código {response.status_code} - Revisa URL y Key en Render."})

        except Exception as e:
            return JsonResponse({'respuesta': f"💀 [CRITICAL_ERROR]: {str(e)}"}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)





def guardar_resena(request, pk):
    if request.method == "POST":
        publicacion = get_object_or_404(Publicacion, pk=pk)
        puntuacion = request.POST.get('puntuacion', 5)
        comentario = request.POST.get('comentario', '')
        
        Resena.objects.update_or_create(
            publicacion=publicacion, 
            autor=request.user,
            defaults={'puntuacion': puntuacion, 'comentario': comentario}
        )
        # Al guardar, te manda directo al "laberinto" de opiniones
        return redirect('ver_opiniones', pk=pk)
