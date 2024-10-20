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
    return render(request, './vistasPublicas/home.html')

def signup(request, extra=None):
    # Verificamos si hay un segmento adicional en la URL (parámetro extra)
    if extra is not None:
        # Si hay un segmento adicional, redirigimos a la página de inicio de sesión
        return redirect('signup')
    
    if request.method == 'GET':
        return render(request, './vistasPublicas/signup.html', {"form": UserCreationForm})
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

        return render(request, './vistasPublicas/signup.html', {
            "form": UserCreationForm, 
            "error": "Passwords did not match."})

@login_required
def private(request, extra=None):
    # Verificamos si hay un segmento adicional en la URL (parámetro extra)
    if extra is not None:
        # Si hay un segmento adicional, redirigimos a la página de inicio de sesión
        return redirect('private')
    return render(request, './vistasPrivadas/private.html')

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
        return render(request, './vistasPublicas/signin.html', {
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
            return render(request, './vistasPublicas/signin.html', {
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
        return redirect('cargar_archivo')
    
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']

            # Recoger los nombres de las columnas ingresados en las cajas de texto
            column_names = [request.POST.get(f'columna_{i + 1}').strip() for i in range(int(request.POST.get('id_num_cajas', 0)))]

            # Validar que no haya columnas vacías
            errors = []  # Lista para almacenar errores
            for i, col in enumerate(column_names):
                if col == "":
                    errors.append(f"Por favor, digite la columna {i + 1} que quiere observar.")

            if errors:
                # Si hay errores, renderizar la plantilla con los errores
                return render(request, 'cargar_archivo.html', {'form': form, 'errors': errors})

            try:
                decoded_file = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(decoded_file, delimiter=';')

                # Verificar si las columnas ingresadas existen en el CSV
                csv_columns = [col.strip() for col in reader.fieldnames]

                if all(col in csv_columns for col in column_names):
                    data = []
                    for row in reader:
                        extracted_row = [row[col] for col in column_names if col in row]
                        data.append(extracted_row)
                else:
                    raise ValueError("Una o más columnas ingresadas no existen en el archivo CSV")

            except Exception as e:
                error_message = f"Error al procesar el archivo: {str(e)}"
                return render(request, './vistasPrivadas/cargar_archivo.html', {'form': form, 'error_message': error_message})

            return render(request, './vistasPrivadas/mostrar_csv.html', {
                'data': data,
                'column_names': column_names
            })

    else:
        form = CSVUploadForm()

    return render(request, './vistasPrivadas/cargar_archivo.html', {'form': form})



def guardar_datos(request):
    if request.method == 'POST':
        # Obtener los datos del input hidden
        data = request.POST.get('data')
        print("Datos recibidos antes de decodificar:", data)

        try:
            data = json.loads(data)
            print("Datos decodificados:", data)
        except json.JSONDecodeError as e:
            print(f"Error al decodificar JSON: {e}")
            return redirect('cargar_archivo')

        for row in data:
            # Verificar si los valores existen antes de asignar
            nombre = row[0] if len(row) > 0 else None
            apellido = row[1] if len(row) > 1 else None
            
            # Guardar solo si 'nombre' y 'apellido' son válidos
            if nombre and apellido:
                Persona.objects.create(nombre=nombre, apellido=apellido)

        # Mostrar un mensaje de éxito
        return redirect('exito_guardado')

    return redirect('cargar_archivo')
 
def exito_guardado(request):
    return render(request, 'exito_guardado.html')
 
