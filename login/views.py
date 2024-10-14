from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, Http404
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import csv
from .forms import CSVUploadForm
import pandas as pd
import io
from .models import Persona
import json

# Create your views here.
def home(request, extra=None):
    # Verificamos si hay un segmento adicional en la URL (parámetro extra)
    if extra is not None:
        # Si hay un segmento adicional, redirigimos a la página de inicio de sesión
        return redirect('home')
    return render(request, 'home.html')

def signup(request, extra=None):
    # Verificamos si hay un segmento adicional en la URL (parámetro extra)
    if extra is not None:
        # Si hay un segmento adicional, redirigimos a la página de inicio de sesión
        return redirect('signup')
    
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('signin')
            except IntegrityError:
                return render(request, 'signup.html', {
                    "form": UserCreationForm, 
                    "error": "Username already exists."})

        return render(request, 'signup.html', {
            "form": UserCreationForm, 
            "error": "Passwords did not match."})

@login_required
def private(request, extra=None):
    # Verificamos si hay un segmento adicional en la URL (parámetro extra)
    if extra is not None:
        # Si hay un segmento adicional, redirigimos a la página de inicio de sesión
        return redirect('private')
    return render(request, 'private.html')

@login_required
def signout(request, extra=None):
    # Verificamos si hay un segmento adicional en la URL (parámetro extra)
    if extra is not None:
        # Si hay un segmento adicional, redirigimos a la página de inicio de sesión
        return redirect('signout')
    logout(request)
    return redirect('home')
    
def signin(request, extra=None):
    # Verificamos si hay un segmento adicional en la URL (parámetro extra)
    if extra is not None:
        # Si hay un segmento adicional, redirigimos a la página de inicio de sesión
        return redirect('signin')

    # Si la solicitud es GET, renderizamos el formulario
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm()
        })

    # Si la solicitud es POST, procesamos los datos del formulario
    elif request.method == 'POST':
        # Autenticamos el usuario con username y password
        user = authenticate(
            request, 
            username=request.POST.get('username'), 
            password=request.POST.get('password')
        )
        
        if user is None:
            # Si el usuario no es válido, renderizamos el formulario con un mensaje de error
            return render(request, 'signin.html', {
                'form': AuthenticationForm(),
                'error': 'Username o contraseña incorrectos.'
            })
        
        # Si el usuario es válido, iniciamos sesión
        login(request, user)
        # Redirigimos a la vista 'private'
        return redirect('private')

    # Si llega un método no esperado, lanzamos un error 404
    raise Http404("Método no válido")
        
def cargar_archivo(request, extra=None):
    if extra is not None:
        # Si hay un segmento adicional, redirigimos a la página de inicio de sesión
        return redirect('cargar_archivo')
    
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']  # Archivo CSV cargado

            # Recoger los nombres de las columnas ingresados en las cajas de texto
            column_names = [request.POST.get(f'columna_{i + 1}').strip() for i in range(int(request.POST.get('id_num_cajas', 0)))]

            print("Nombres de columnas recibidos:", column_names)  # Para depurar

            # Validar que no haya columnas vacías
            if any(col == "" for col in column_names):
                error_message = "Por favor, digite la columna que quiere observar."
                return render(request, 'cargar_archivo.html', {'form': form, 'error_message': error_message})

            try:
                # Lee el archivo CSV con el delimitador correcto
                decoded_file = csv_file.read().decode('ISO-8859-1').splitlines()
                # Usar `delimiter=';'` si el CSV está separado por punto y coma
                reader = csv.DictReader(decoded_file, delimiter=';')  # Cambiado para incluir el delimitador

                # Verificar si las columnas ingresadas existen en el CSV
                csv_columns = [col.strip() for col in reader.fieldnames]  # Quitar espacios en blanco de las columnas
                print("Columnas en el CSV:", csv_columns)  # Para depurar

                if all(col in csv_columns for col in column_names):
                    data = []
                    for row in reader:
                        # Extraer los valores de las columnas especificadas
                        extracted_row = [row[col] for col in column_names if col in row]
                        data.append(extracted_row)

                else:
                    raise ValueError("Una o más columnas ingresadas no existen en el archivo CSV")

            except Exception as e:
                error_message = f"Error al procesar el archivo: {str(e)}"
                return render(request, 'cargar_archivo.html', {'form': form, 'error_message': error_message})

            # Mostrar los datos extraídos en la plantilla
            return render(request, 'mostrar_csv.html', {
                'data': data,  # Datos de las columnas extraídas
                'column_names': column_names  # Columnas que se mostraron
            })

    else:
        form = CSVUploadForm()

    return render(request, 'cargar_archivo.html', {'form': form})

def guardar_datos(request):
    if request.method == 'POST':
        # Obtener los datos del input hidden
        data = request.POST.get('data')
        data = json.loads(data)

        for row in data:
            # Asumiendo que el primer valor es 'nombre' y el segundo es 'apellido'
            nombre = row[0]
            apellido = row[1]

            # Guardar cada fila en la base de datos
            Persona.objects.create(nombre=nombre, apellido=apellido)

        # Mostrar un mensaje de éxito
        return redirect('exito_guardado')

    return redirect('cargar_archivo')
 
def exito_guardado(request):
    return render(request, 'exito_guardado.html')
 
