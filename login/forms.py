from django import forms

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