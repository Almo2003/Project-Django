# Importa el módulo de formularios de Django
from django import forms

# Importa los modelos Trazabilidad, Egresado e Imagen desde models.py
from .models import Trazabilidad, Egresado, Imagen

# Formulario para la carga de archivos CSV
class CSVUploadForm(forms.Form):
    # Campo para cargar un archivo CSV
    csv_file = forms.FileField(
        label='Cargar archivo CSV', 
        widget=forms.FileInput(attrs={'accept': '.csv'}),  # Acepta únicamente archivos con extensión .csv
        required=False  # No es obligatorio
    )
    # Campo para ingresar el número de cajas de texto
    num_cajas = forms.IntegerField(
        label='Número de cajas de texto', 
        min_value=1,  # El valor mínimo permitido es 1
        required=True  # Este campo es obligatorio
    )

    # Método de validación para el archivo CSV
    def clean_csv_file(self):
        file = self.cleaned_data.get('csv_file')  # Obtiene el archivo del formulario
        # Valida si el archivo tiene extensión .csv
        if file and not file.name.endswith('.csv'):
            raise forms.ValidationError("El archivo debe tener extensión .csv")
        return file  # Devuelve el archivo si pasa la validación

# Formulario para el modelo Trazabilidad
class TrazabilidadForm(forms.ModelForm):
    class Meta:
        model = Trazabilidad  # Especifica el modelo asociado
        fields = ['ubicacion_laboral', 'correoelectronico', 'telefono', 'oferta']  # Campos incluidos en el formulario

    # Campos personalizados con widgets y etiquetas
    ubicacion_laboral = forms.CharField(
        max_length=100, 
        label="Ubicación Laboral", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la ubicación laboral'})
    )
    correoelectronico = forms.EmailField(
        label="Correo Electrónico", 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el correo electrónico'})
    )
    telefono = forms.CharField(
        max_length=15, 
        label="Teléfono", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono'})
    )
    oferta = forms.CharField(
        max_length=200, 
        label="Oferta", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la oferta'})
    )

# Formulario para el modelo Egresado
class EgresadoForm(forms.ModelForm):
    class Meta:
        model = Egresado  # Especifica el modelo asociado
        fields = ['nombre', 'profesion', 'ano_grado', 'cargo_actual', 'correo', 
                  'descripcion', 'trayectoria', 'datos_adicionales', 'Imagen']  # Campos incluidos en el formulario

# Formulario adicional para destacar egresados
class EgresadoDestacadoForm(forms.ModelForm):
    class Meta:
        model = Egresado  # Especifica el modelo asociado
        fields = ['nombre', 'profesion', 'ano_grado', 'cargo_actual', 'correo', 
                  'descripcion', 'trayectoria', 'datos_adicionales', 'Imagen']  # Campos incluidos

# Formulario para el modelo Imagen
class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen  # Especifica el modelo asociado
        fields = ['imagen']  # Solo incluye el campo de la imagen

    # Método de validación para el campo de imagen
    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')  # Obtiene la imagen del formulario
        
        # Verifica si el archivo tiene una extensión válida
        if imagen:
            if not imagen.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                raise forms.ValidationError('Formato de imagen no soportado. Solo se aceptan PNG, JPG, JPEG o GIF.')
        
        return imagen  # Devuelve la imagen si pasa la validación
