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
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            num_cajas = form.cleaned_data['num_cajas']

            # Leer el archivo CSV
            data = []
            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
            except UnicodeDecodeError:
                decoded_file = csv_file.read().decode('ISO-8859-1').splitlines()

            reader = csv.reader(decoded_file)

            # Leer los datos y asegurarse de que hay al menos dos columnas
            nombres = []  # Lista para almacenar nombres y apellidos
            for row in reader:
                # Verificar que la fila tenga al menos dos columnas
                if len(row) < 2:
                    continue  # O salta a la siguiente fila si no hay suficientes datos

                nombre = row[0].strip()  # Columna de nombres
                apellido = row[1].strip()  # Columna de apellidos
                nombres.append((nombre, apellido))

            # Redirigir a la vista donde se muestra el contenido del archivo
            return render(request, 'mostrar_csv.html', {'nombres': nombres})

    else:
        form = CSVUploadForm()

    return render(request, 'cargar_archivo.html', {'form': form})
    
    
    
 
 
