import os
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# ==========================================================
# 🛰️ DETECTOR DE ENTORNO (SISTEMA NEÓN)
# ==========================================================
IS_RENDER = 'RENDER' in os.environ

# ==========================================================
# 👤 1. PERFIL: Datos del operador
# ==========================================================
class Perfil(models.Model):
    PREFIJOS = [
        ('503', 'SV +503'),
        ('502', 'GT +502'),
        ('504', 'HN +504'),
        ('505', 'NI +505'),
        ('506', 'CR +506'),
        ('1', 'USA +1'),
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    nombre = models.CharField(max_length=100, blank=True, null=True)
    
    if IS_RENDER:
        foto_perfil = CloudinaryField('image', folder='perfiles', blank=True, null=True)
    else:
        foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    
    prefijo = models.CharField(max_length=5, choices=PREFIJOS, default='503')
    telefono = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(max_length=254, blank=True, null=True)
    direccion = models.CharField(max_length=250, blank=True, null=True)
    fecha_unido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Operador: {self.usuario.username}"

# ==========================================================
# 📂 2. CATEGORÍAS
# ==========================================================
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    def __str__(self): 
        return self.nombre

# ==========================================================
# 💎 3. PUBLICACIÓN: El núcleo del sistema (UPGRADED)
# ==========================================================
class Publicacion(models.Model):
    TIPO_NEGOCIO = [
        ('VENTA', 'Venta'),
        ('ALQUILER', 'Alquiler'),
        ('CAMBIO', 'Cambio / Permuta'),
        ('SERVICIO','Servicio')
    ]
    ESTADO_ITEM = [
        ('NUEVO', 'Nuevo'),
        ('USADO', 'Usado'),
    ]

    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mis_publicaciones')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=255, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    precio = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True) 
    
    # ⚡ FOTO PRINCIPAL
    if IS_RENDER:
        foto = CloudinaryField('image', folder='productos', blank=True, null=True)
    else:
        foto = models.ImageField(upload_to='productos/', blank=True, null=True)
    
    # 🛰️ MÓDULO AR (REALIDAD AUMENTADA)
    # Usamos 'raw' en Cloudinary para archivos .glb (3D)
    if IS_RENDER:
        modelo_3d = CloudinaryField('raw', folder='modelos_3d', blank=True, null=True)
    else:
        modelo_3d = models.FileField(upload_to='modelos_3d/', blank=True, null=True)

    # 🔗 MÓDULO BLOCKCHAIN
    # Para guardar el hash del Smart Contract o ID de transacción
    contract_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID Contrato Blockchain")

    tipo_negocio = models.CharField(max_length=10, choices=TIPO_NEGOCIO, blank=True, null=True)
    estado_fisico = models.CharField(max_length=10, choices=ESTADO_ITEM, blank=True, null=True)
    vendido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    vistas = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        estado = 'VENDIDO' if self.vendido else 'ACTIVO'
        return f"{self.titulo} - {estado}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detalle', args=[str(self.id)])

    @property
    def promedio_estrellas(self):
        # Lógica para calcular el promedio dinámicamente
        resenas = self.resenas.all()
        if resenas.exists():
            total = sum(r.puntuacion for r in resenas)
            return round(total / resenas.count(), 1)
        return 0.0

    @property
    def total_resenas(self):
        return self.resenas.count()

# ==========================================================
# 🖼️ 4. GALERÍA ADICIONAL
# ==========================================================
class Imagen(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='fotos')
    
    if IS_RENDER:
        imagen = CloudinaryField('image', folder='productos_galeria', null=True, blank=True)
    else:
        imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return f"Imagen de {self.publicacion.titulo}"

# ==========================================================
# ⭐ 5. RESEÑAS: Sistema de Calificaciones (Otto-task)
# ==========================================================
class Resena(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.CASCADE, related_name='resenas')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    puntuacion = models.IntegerField(default=5)
    comentario = models.TextField(max_length=500, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_creacion']
        unique_together = ('publicacion', 'autor')

    def __str__(self):
        return f"{self.puntuacion}⭐ por {self.autor.username}"

