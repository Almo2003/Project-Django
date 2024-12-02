from django import forms
from .models import Trazabilidad, Egresado

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Cargar archivo CSV', 
                               widget=forms.FileInput(attrs={'accept': '.csv'}), 
                               required=False)
    num_cajas = forms.IntegerField(label='Número de cajas de texto', 
                                    min_value=1, required=True)

    def clean_csv_file(self):
        file = self.cleaned_data.get('csv_file')
        if file and not file.name.endswith('.csv'):
            raise forms.ValidationError("El archivo debe tener extensión .csv")
        return file
    
class TrazabilidadForm(forms.ModelForm):
    class Meta:
        model = Trazabilidad
        fields = ['ubicacion_laboral', 'correoelectronico', 'telefono', 'oferta']

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

class EgresadoForm(forms.ModelForm):
    class Meta:
        model = Egresado
        fields = ['nombre', 'profesion', 'ano_grado', 'cargo_actual', 'correo', 'descripcion', 'trayectoria', 'datos_adicionales', 'imagen_url']