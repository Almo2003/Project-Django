from django import forms
from .models import Trasabilidad

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
    

class TrasabilidadForm(forms.ModelForm):
    class Meta:
        model = Trasabilidad
        fields = ['telefono', 'correo', 'ubicacion', 'oferta']
        labels = {
            'telefono': 'Teléfono',
            'correo': 'Correo Electrónico',
            'ubicacion': 'Ubicación',
            'oferta': 'Oferta Laboral',
        }
        widgets = {
            'telefono': forms.TextInput(attrs={'placeholder': 'Ej. 3001234567'}),
            'correo': forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'}),
            'ubicacion': forms.TextInput(attrs={'placeholder': 'Ciudad o Dirección'}),
            'oferta': forms.Textarea(attrs={'placeholder': 'Detalles de la oferta', 'rows': 3}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.isdigit():
            raise forms.ValidationError("El teléfono debe contener solo números.")
        return telefono