from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q, Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from io import StringIO
import requests
import json
import os

from .models import Publicacion, Categoria, Imagen, Perfil, Resena
from .forms import PublicacionForm, PerfilForm

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
def home(request):
    nodos_activos, trafico_total = obtener_conteo_red()
    query = request.GET.get('q', '').strip()
    categorias = Categoria.objects.all()

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
    anuncio = get_object_or_404(Publicacion, pk=pk)
    anuncio.vistas = (anuncio.vistas or 0) + 1
    anuncio.save()

    resenas = anuncio.resenas.all()
    total = resenas.count()
    promedio_data = resenas.aggregate(Avg('puntuacion'))['puntuacion__avg']
    promedio = round(promedio_data, 1) if promedio_data else 0.0

    return render(request, 'detalle.html', {
        'anuncio': anuncio, 
        'galeria': anuncio.fotos.all(),
        'promedio': promedio,
        'total': total
    })

# --- 3. ESTADÍSTICAS Y GESTIÓN ---
def stats_global(request):
    total_db = Publicacion.objects.count()
    hace_5_min = timezone.now() - timedelta(minutes=5)
    online_real = User.objects.filter(last_login__gte=hace_5_min).count()
    total_vistas = Publicacion.objects.aggregate(total=Sum('vistas'))['total'] or 0
    categorias_reales = Categoria.objects.annotate(num=Count('publicacion'))

    return render(request, 'stats.html', {
        'total': total_db, 'activos': online_real, 'vistas': total_vistas, 'categorias': categorias_reales
    })

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

@login_required
def vender_producto(request):
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
def perfil(request):
    return render(request, 'perfil.html', {'mis_anuncios': Publicacion.objects.filter(vendedor=request.user).order_by('-fecha_creacion')})

@login_required
def marcar_vendido(request, anuncio_id):
    anuncio = get_object_or_404(Publicacion, id=anuncio_id, vendedor=request.user)
    anuncio.vendido = True
    anuncio.save()
    return JsonResponse({'status': 'ok', 'message': 'Vendido correctamente'})

def obtener_conteo_red():
    limite = timezone.now() - timedelta(minutes=10)
    online = User.objects.filter(last_login__gte=limite).count()
    total_vistas = Publicacion.objects.aggregate(total=Sum('vistas'))['total'] or 0
    return online, total_vistas

@login_required
def editar_perfil(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, "PERFIL_ACTUALIZADO")
            return redirect('perfil')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'editar_perfil.html', {'form': form})

def restaurar_backup(request):
    if request.method == 'POST' and request.FILES.get('backup_file'):
        backup_file = request.FILES['backup_file']
        with open('temp_backup.json', 'wb+') as destination:
            for chunk in backup_file.chunks():
                destination.write(chunk)
        try:
            from django.core.management import call_command
            call_command('loaddata', 'temp_backup.json')
            messages.success(request, "NÚCLEO REESTABLECIDO [✅]")
        except Exception as e:
            messages.error(request, f"ERROR: {e}")
    return redirect('dashboard')

# --- 4. PROTOCOLO SHADOW (AI) ---
@csrf_exempt
def bot_consulta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            texto = data.get('texto', '').strip()

            # ESCÁNER DINÁMICO: Filtra por el texto exacto del botón o búsqueda
            # Ahora busca específicamente en el nombre de la categoría
            productos = Publicacion.objects.filter(
                Q(categoria__nombre__icontains=texto) | Q(titulo__icontains=texto),
                vendido=False
            )[:5]

            if productos:
                res = f"⚡ **OTTO-MARKET // {texto.upper()}** ⚡<br>"
                for p in productos:
                    res += f"📦 **{p.titulo.upper()}** - ${p.precio}<br>"
                return JsonResponse({'respuesta': res})
            
            # Si no hay productos, intentamos con el Agente (Gumloop)
            # URL_GUMLOOP = "AQUÍ_VA_TU_NUEVO_WEBHOOK" 
            return JsonResponse({'respuesta': f"🔍 No hay suministros en **{texto}** por ahora."})

        except Exception as e:
            return JsonResponse({'respuesta': f"💀 [FALLO_NEURAL]: {str(e)}"})
    return JsonResponse({'error': 'Método no permitido'}, status=405)






def pagina_bot(request):
    return render(request, 'bot_consulta.html')

def ver_opiniones(request, pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    if request.method == "POST":
        puntos = request.POST.get('puntuacion', 5)
        texto = request.POST.get('comentario', '')
        if texto:
            Resena.objects.update_or_create(
                publicacion=publicacion, autor=request.user,
                defaults={'puntuacion': int(puntos), 'comentario': texto}
            )
            return redirect('ver_opiniones', pk=pk)

    resenas = publicacion.resenas.all()
    total = resenas.count()
    promedio_data = resenas.aggregate(Avg('puntuacion'))['puntuacion__avg']
    promedio = round(promedio_data, 1) if promedio_data else 0.0

    def get_pct(n):
        return (resenas.filter(puntuacion=n).count() / total * 100) if total > 0 else 0

    return render(request, 'opiniones.html', {
        'publicacion': publicacion, 'resenas': resenas, 'promedio': promedio, 'total': total,
        'b5': get_pct(5), 'b4': get_pct(4), 'b3': get_pct(3), 'b2': get_pct(2), 'b1': get_pct(1),
    })

def guardar_resena(request, pk):
    if request.method == "POST":
        publicacion = get_object_or_404(Publicacion, pk=pk)
        puntuacion = request.POST.get('puntuacion', 5)
        comentario = request.POST.get('comentario', '')
        Resena.objects.update_or_create(
            publicacion=publicacion, autor=request.user,
            defaults={'puntuacion': puntuacion, 'comentario': comentario}
        )
        return redirect('ver_opiniones', pk=pk)

@login_required
def gestionar_anuncio(request, pk):
    anuncio = get_object_or_404(Publicacion, pk=pk, vendedor=request.user)
    if request.method == 'POST':
        form = PublicacionForm(request.POST, request.FILES, instance=anuncio)
        if form.is_valid():
            form.save()
            messages.success(request, "UNIDAD_MODIFICADA")
            return redirect('perfil')
    else:
        form = PublicacionForm(instance=anuncio)
    return render(request, 'vender_hardware.html', {'form': form, 'editando': True})

@login_required
def eliminar_anuncio(request, pk):
    anuncio = get_object_or_404(Publicacion, pk=pk, vendedor=request.user)
    anuncio.delete()
    messages.warning(request, "UNIDAD_ELIMINADA")
    return redirect('perfil')

@login_required
def reactivar_anuncio(request, anuncio_id):
    anuncio = get_object_or_404(Publicacion, id=anuncio_id, vendedor=request.user)
    anuncio.vendido = False
    anuncio.save()
    return redirect('perfil')

def descargar_backup(request):
    from django.core.management import call_command
    from django.http import HttpResponse
    output = StringIO()
    call_command('dumpdata', 'marketapp', indent=2, stdout=output)
    response = HttpResponse(output.getvalue(), content_type="application/json")
    response['Content-Disposition'] = 'attachment; filename="backup_otto.json"'
    return response

