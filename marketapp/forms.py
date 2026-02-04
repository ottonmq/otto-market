from django import forms
from .models import Perfil, Publicacion, Categoria

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        # Incluimos PREFIJO para el WhatsApp internacional
        fields = ['nombre', 'foto_perfil', 'prefijo', 'telefono', 'correo', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control bg-dark text-info border-info', 'placeholder': '>> AGENT_NAME'}),
            'foto_perfil': forms.FileInput(attrs={'class': 'form-control bg-dark text-info border-info'}),
            'prefijo': forms.Select(attrs={'class': 'form-select bg-dark text-info border-info'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control bg-dark text-info border-info', 'placeholder': '>> LINE_PHONE'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control bg-dark text-info border-info', 'placeholder': '>> USER_MAIL'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control bg-dark text-info border-info', 'placeholder': '>> SECTOR_LOCATION'}),
        }

    def __init__(self, *args, **kwargs):
        super(PerfilForm, self).__init__(*args, **kwargs)
        self.fields['correo'].required = False
        self.fields['nombre'].required = True  # Para saber quién publica

class PublicacionForm(forms.ModelForm):
    class Meta:
        model = Publicacion
        # EL TELÉFONO YA NO ESTÁ AQUÍ (Se jala del perfil)
        fields = [
            'categoria', 'titulo', 'marca', 'modelo', 'precio', 
            'descripcion', 'foto', 'tipo_negocio', 'estado_fisico'
        ]
        labels = {
            'categoria': 'SELECCIONAR_AREA',
            'titulo': 'NOMBRE_DEL_PRODUCTO_O_SERVICIO',
            'marca': 'FABRICANTE_O_MARCA',
            'modelo': 'VERSION_O_MODELO',
            'precio': 'VALOR_DE_PRODUCTO ($)',
            'descripcion': 'ESPECIFICACIONES_TECNICAS',
            'foto': 'CARGAR__IMAGENL',
            'tipo_negocio': 'MODALIDAD_DE_TRATO',
            'estado_fisico': 'INTEGRIDAD_DEL_ITEM',
        }
        
    def __init__(self, *args, **kwargs):
        super(PublicacionForm, self).__init__(*args, **kwargs)
        
        # 🔓 PRECIO OPCIONAL
        self.fields['precio'].required = False

        # 🔧 LIMPIEZA DE RAYAS EN SELECTORES (CHOICES)
        # Diccionario con los campos y el texto que querés mostrar
        selectores = {
            'categoria': '>> SELECCIONAR_CATEGORIA',
            'tipo_negocio': '>> MODALIDAD_DE_TRATO',
            'estado_fisico': '>> INTEGRIDAD_DEL_ITEM'
        }

        for campo, texto in selectores.items():
            if campo in self.fields:
                # Quitamos las rayas [0] y ponemos nuestro texto
                opciones = list(self.fields[campo].choices)
                opciones[0] = ('', texto) 
                self.fields[campo].choices = opciones

        
        
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-select bg-dark text-info border-info'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control bg-dark text-warning border-warning', 'placeholder': '>> ITEM_ID'}),
            'marca': forms.TextInput(attrs={'class': 'form-control bg-dark text-info border-info'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control bg-dark text-info border-info'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control bg-dark text-success border-success'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control bg-dark text-info border-info', 'rows': 3}),
            'foto': forms.FileInput(attrs={'class': 'form-control bg-dark text-info border-info'}),
            'tipo_negocio': forms.Select(attrs={'class': 'form-select bg-dark text-info border-info'}),
            'estado_fisico': forms.Select(attrs={'class': 'form-select bg-dark text-info border-info'}),
        }

    def __init__(self, *args, **kwargs):
        super(PublicacionForm, self).__init__(*args, **kwargs)
        # 🔓 LIBERANDO PRECIO
        self.fields['precio'].required = False
        # ❌ AQUÍ ESTABA EL ERROR: No intentamos liberar 'telefono' porque ya no está en 'fields'
