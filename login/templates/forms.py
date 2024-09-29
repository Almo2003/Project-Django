
from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Cargar archivo CSV', widget=forms.FileInput(attrs={'accept': '.csv'}))

    def clean_csv_file(self):
        file = self.cleaned_data['csv_file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError("El archivo debe tener extensión .csv")
        return file
