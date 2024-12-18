from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import csv
from .forms import CSVUploadForm, TrazabilidadForm, EgresadoForm, EgresadoDestacadoForm, ImagenForm
import pandas as pd
import io, os
from .models import Persona, Trazabilidad, Egresado, Imagen
import json
from django.core.files.storage import FileSystemStorage
from django.conf import settings

# Create your views here.
def home(request, extra=None):
    # Obtenemos todos los objetos de Imagen y Egresado
    imagenes = Imagen.objects.all()
    egresados = Egresado.objects.all()
    
    # Verificamos si hay un segmento adicional en la URL (parámetro extra)
    if extra is not None:
        # Si hay un segmento adicional, redirigimos a la página de inicio de sesión
        return redirect('home')
    
    # Combinamos los contextos en un solo diccionario
    context = {
        'imagenes': imagenes,
        'egresados': egresados
    }
    
    return render(request, './vistasPublicas/home.html', context)

# Función para registrar nuevos usuarios
def signup(request, extra=None):
    # Verificamos si hay un segmento adicional en la URL (parámetro extra)
    if extra is not None:
        # Si hay un segmento adicional, redirigimos a la página de registro para evitar rutas no deseadas
        return redirect('signup')
    
    # Si la solicitud es GET, renderizamos el formulario de registro
    if request.method == 'GET':
        return render(request, './vistasPublicas/signup.html', {"form": UserCreationForm})
    else:  # Si la solicitud es POST
        # Verificamos si las contraseñas coinciden
        if request.POST["password1"] == request.POST["password2"]:
            try:
                # Creamos un nuevo usuario con el username y la contraseña proporcionados
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()  # Guardamos el usuario en la base de datos
                login(request, user)  # Iniciamos sesión automáticamente
                return redirect('signin')  # Redirigimos al inicio de sesión
            except IntegrityError:
                # Si ocurre un error (como un nombre de usuario duplicado), mostramos un mensaje de error
                return render(request, 'signup.html', {
                    "form": UserCreationForm, 
                    "error": "Username already exists."
                })

        # Si las contraseñas no coinciden, renderizamos el formulario con un mensaje de error
        return render(request, './vistasPublicas/signup.html', {
            "form": UserCreationForm, 
            "error": "Passwords did not match."
        })

# Vista privada protegida con @login_required
@login_required
def private(request, extra=None):
    # Verificamos si hay un segmento adicional en la URL
    if extra is not None:
        # Si existe, redirigimos nuevamente a la página privada
        return redirect('private')
    # Renderizamos la plantilla de la vista privada
    return render(request, './vistasPrivadas/private.html')

# Función para cerrar sesión
@login_required
def signout(request, extra=None):
    # Verificamos si hay un segmento adicional en la URL
    if extra is not None:
        # Si existe, redirigimos nuevamente a la función de cierre de sesión
        return redirect('signout')
    # Cerramos la sesión del usuario
    logout(request)
    # Redirigimos a la página principal
    return redirect('home')

# Función para iniciar sesión
def signin(request, extra=None):
    # Verificamos si hay un segmento adicional en la URL
    if extra is not None:
        # Si existe, redirigimos a la función de inicio de sesión
        return redirect('signin')

    # Si la solicitud es GET, renderizamos el formulario de inicio de sesión
    if request.method == 'GET':
        return render(request, './vistasPublicas/signin.html', {
            'form': AuthenticationForm()
        })

    # Si la solicitud es POST, procesamos los datos enviados
    elif request.method == 'POST':
        # Autenticamos al usuario con el username y password proporcionados
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
        
        # Si la autenticación es exitosa, iniciamos sesión
        login(request, user)
        # Redirigimos a la vista privada
        return redirect('private')

    # Si el método no es válido, lanzamos un error 404
    raise Http404("Método no válido")

# Función para cargar un archivo CSV
@login_required    
def cargar_archivo(request, extra=None):
    # Verificamos si hay un segmento adicional en la URL
    if extra is not None:
        # Si existe, redirigimos nuevamente a la función de carga
        return redirect('cargar_archivo')
    
    if request.method == 'POST':  # Si la solicitud es POST
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Obtenemos el archivo CSV cargado
            csv_file = request.FILES['csv_file']

            # Obtenemos los nombres de las columnas especificadas por el usuario
            column_names = [request.POST.get(f'columna_{i + 1}').strip() for i in range(int(request.POST.get('id_num_cajas', 0)))]

            # Validamos que no haya columnas vacías
            errors = []  # Lista para almacenar los errores
            for i, col in enumerate(column_names):
                if col == "":
                    errors.append(f"Por favor, digite la columna {i + 1} que quiere observar.")

            if errors:
                # Si hay errores, los mostramos al usuario
                return render(request, './vistasPrivadas/cargar_archivo.html', {'form': form, 'errors': errors})

            try:
                # Procesamos el archivo CSV
                decoded_file = csv_file.read().decode('ISO-8859-1').splitlines()
                reader = csv.DictReader(decoded_file, delimiter=';')

                # Verificamos que las columnas ingresadas existan en el archivo CSV
                csv_columns = [col.strip() for col in reader.fieldnames]

                if all(col in csv_columns for col in column_names):
                    # Extraemos los datos de las columnas seleccionadas
                    data = []
                    for row in reader:
                        extracted_row = [row[col] for col in column_names if col in row]
                        data.append(extracted_row)
                else:
                    # Si las columnas no existen, lanzamos un error
                    raise ValueError("Una o más columnas ingresadas no existen en el archivo CSV")

            except Exception as e:
                # Si ocurre un error al procesar el archivo, lo mostramos al usuario
                error_message = f"Error al procesar el archivo: {str(e)}"
                return render(request, './vistasPrivadas/cargar_archivo.html', {'form': form, 'error_message': error_message})

            # Si todo es exitoso, renderizamos la vista para mostrar los datos del CSV
            return render(request, './vistasPrivadas/mostrar_csv.html', {
                'data': data,
                'column_names': column_names
            })

    else:  # Si la solicitud es GET
        form = CSVUploadForm()

    # Renderizamos el formulario para cargar un archivo
    return render(request, './vistasPrivadas/cargar_archivo.html', {'form': form})

# Función para guardar los datos en la base de datos
@login_required
def guardar_datos(request):
    if request.method == 'POST':  # Solo permitimos POST
        # Obtenemos los datos desde el input oculto
        data = request.POST.get('data')
        print("Datos recibidos antes de decodificar:", data)

        try:
            # Decodificamos los datos del JSON
            data = json.loads(data)
            print("Datos decodificados:", data)
        except json.JSONDecodeError as e:
            # Si hay un error al decodificar, redirigimos a la vista de carga
            print(f"Error al decodificar JSON: {e}")
            return redirect('cargar_archivo')

        for row in data:
            # Verificamos y asignamos los valores de cada columna
            nombre = row[0] if len(row) > 0 else None
            documento = row[1] if len(row) > 1 else None
            programa = row[2] if len(row) > 2 else None
            fechagrado = row[3] if len(row) > 3 else None
            ubicacion_laboral = row[4] if len(row) > 4 else None
            correoelectronico = row[5] if len(row) > 5 else None
            telefono = row[6] if len(row) > 6 else None
            oferta = row[7] if len(row) > 7 else None

            # Verificamos si ya existe un registro con el mismo documento
            if documento and not Persona.objects.filter(documento=documento).exists():
                try:
                    # Creamos y guardamos un nuevo registro en Persona
                    persona = Persona(
                        nombre=nombre,
                        documento=documento,
                        programa=programa,
                        fechagrado=fechagrado
                    )
                    persona.save()

                    # Creamos un registro en Trazabilidad si hay datos dinámicos
                    if telefono or correoelectronico or ubicacion_laboral or oferta:
                        trazabilidad = Trazabilidad(
                            persona=persona,
                            telefono=telefono,
                            correoelectronico=correoelectronico,
                            ubicacion_laboral=ubicacion_laboral,
                            oferta=oferta
                        )
                        trazabilidad.save()

                except IntegrityError as e:
                    print(f"Error al guardar datos: {e}")
            else:
                # Si el registro ya existe, lo ignoramos
                print(f"Registro duplicado encontrado para documento: {documento}")

        # Redirigimos a una vista de éxito tras guardar los datos
        return redirect('exito_guardado')

    # Si el método no es POST, redirigimos a la vista de carga
    return redirect('cargar_archivo')

# Función para mostrar el mensaje de éxito
def exito_guardado(request):
    return render(request, 'exito_guardado.html')

# Función para buscar una persona por su documento
@login_required
def buscar(request):
    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST
        documento = request.POST.get('documento')  # Obtiene el documento del formulario enviado por el usuario

        try:
            # Busca una persona en la base de datos con el documento proporcionado
            persona = Persona.objects.get(documento=documento)

            # Busca todas las trazabilidades asociadas a esta persona
            trazabilidades = Trazabilidad.objects.filter(persona=persona)

            # Renderiza la vista con los resultados encontrados
            return render(request, './vistasPrivadas/buscar_resultado.html', {
                'persona': persona,
                'trazabilidades': trazabilidades,
            })
        except Persona.DoesNotExist:
            # Si no se encuentra ninguna persona con ese documento, se muestra un mensaje de error
            error_message = f"No se encontró ninguna persona con el documento {documento}."
            return render(request, './vistasPrivadas/buscarpersona.html', {'error_message': error_message})

    # Si la solicitud no es POST, renderiza el formulario para buscar personas
    return render(request, './vistasPrivadas/buscarpersona.html')

# Función para ver el historial de trazabilidad de una persona
@login_required
def ver_trazabilidad(request, documento):
    # Busca la persona en la base de datos por su documento
    persona = get_object_or_404(Persona, documento=documento)

    # Obtiene todas las trazabilidades asociadas a esta persona
    trazabilidades = persona.trazabilidades.all()

    # Renderiza la vista de trazabilidad con los datos de la persona y su historial
    context = {
        'persona': persona,
        'trazabilidades': trazabilidades,
    }
    return render(request, './vistasPrivadas/ver_trazabilidad.html', context)

# Función para mostrar el detalle de una persona y su trazabilidad
@login_required
def detalle_persona(request, documento):
    # Busca la persona en la base de datos por su documento
    persona = get_object_or_404(Persona, documento=documento)

    # Obtiene todas las trazabilidades asociadas a esta persona
    trazabilidades = Trazabilidad.objects.filter(persona=persona)

    # Renderiza la vista con los detalles de la persona y su trazabilidad
    contexto = {
        'persona': persona,
        'trazabilidades': trazabilidades,
    }
    return render(request, './vistasPrivadas/buscar_resultado.html', contexto)

# Función para agregar un nuevo registro de trazabilidad para una persona
@login_required
def agregar_trazabilidad(request, documento):
    # Busca la persona en la base de datos por su documento
    persona = get_object_or_404(Persona, documento=documento)

    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST
        form = TrazabilidadForm(request.POST)  # Crea el formulario con los datos enviados
        if form.is_valid():
            # Crea un nuevo registro de trazabilidad asociado a la persona
            Trazabilidad.objects.create(
                persona=persona,
                ubicacion_laboral=form.cleaned_data['ubicacion_laboral'],
                correoelectronico=form.cleaned_data['correoelectronico'],
                telefono=form.cleaned_data['telefono'],
                oferta=form.cleaned_data['oferta'],
            )
            # Redirige al detalle de la persona después de guardar
            return redirect('buscar_resultado', documento=documento)
    else:
        # Si la solicitud no es POST, muestra un formulario vacío
        form = TrazabilidadForm()

    # Renderiza la vista para agregar trazabilidad
    return render(request, './vistasPrivadas/agregar_trazabilidad.html', {'form': form, 'persona': persona})

# Función para modificar un registro de trazabilidad existente
@login_required
def modificar_trazabilidad(request, trazabilidad_id):
    # Busca el registro de trazabilidad por su ID
    trazabilidad = get_object_or_404(Trazabilidad, id=trazabilidad_id)

    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST
        # Crea el formulario con los datos enviados y asocia el registro de trazabilidad existente
        form = TrazabilidadForm(request.POST, instance=trazabilidad)
        if form.is_valid():
            form.save()  # Guarda los cambios realizados
            # Redirige a la vista de trazabilidad de la persona
            return redirect('ver_trazabilidad', documento=trazabilidad.persona.documento)
    else:
        # Si la solicitud no es POST, carga el formulario con los datos existentes
        form = TrazabilidadForm(instance=trazabilidad)

    # Renderiza la vista para modificar trazabilidad
    return render(request, './vistasPrivadas/agregar_trazabilidad.html', {'form': form, 'persona': trazabilidad.persona})

# Función para eliminar un registro de trazabilidad
@login_required
def eliminar_trazabilidad(request, trazabilidad_id):
    # Busca el registro de trazabilidad por su ID
    trazabilidad = get_object_or_404(Trazabilidad, id=trazabilidad_id)

    # Obtiene el documento de la persona asociada para redirigir después
    documento = trazabilidad.persona.documento

    # Elimina el registro de trazabilidad
    trazabilidad.delete()

    # Redirige a la vista de trazabilidad de la persona
    return redirect('ver_trazabilidad', documento=documento)

# Función para gestionar los egresados destacados
@login_required
def egresadosDestacados(request):
    egresados = Egresado.objects.all()  # Obtiene todos los egresados destacados

    if request.method == "POST":  # Verifica si la solicitud es de tipo POST
        if len(egresados) >= 3:
            # Si ya hay 3 egresados destacados, muestra un mensaje de error
            messages.error(request, "No puedes agregar más de 3 egresados destacados.")
        else:
            form = EgresadoDestacadoForm(request.POST, request.FILES)  # Crea el formulario con los datos enviados
            if form.is_valid():
                form.save()  # Guarda el nuevo egresado destacado
                messages.success(request, "Egresado destacado agregado correctamente.")
                return redirect('egresadosDestacados')
            else:
                messages.error(request, "Error al guardar el egresado destacado.")
    else:
        # Si la solicitud no es POST, muestra un formulario vacío
        form = EgresadoDestacadoForm()

    # Renderiza la vista de gestión de egresados destacados
    return render(request, './vistasPrivadas/egresadosDestacados.html', {'egresados': egresados, 'form': form})

# Función para listar los egresados destacados públicamente
def listar_egresados_destacados(request):
    egresados = Egresado.objects.all()  # Obtiene todos los egresados destacados
    return render(request, 'listar_egresados_destacados.html', {'egresados': egresados})

# Función para editar un egresado destacado
@login_required
def editar_egresado(request, id):
    egresado = get_object_or_404(Egresado, id=id)  # Busca el egresado por su ID

    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST
        form = EgresadoDestacadoForm(request.POST, request.FILES, instance=egresado)
        if form.is_valid():
            form.save()  # Guarda los cambios realizados
            return redirect('egresadosDestacados')
    else:
        # Si la solicitud no es POST, carga el formulario con los datos existentes
        form = EgresadoDestacadoForm(instance=egresado)

    # Renderiza la vista para editar egresados destacados
    return render(request, './vistasPrivadas/editarEgresado.html', {'form': form, 'egresado': egresado})

# Función para ver los detalles de un egresado destacado
@login_required
def egresado_detalle(request, egresado_id):
    egresado = Egresado.objects.get(id=egresado_id)  # Obtiene el egresado por su ID
    return render(request, './vistasPrivadas/egresado_detalle.html', {'egresado': egresado})

# Función para cargar imágenes
def cargar_imagenes(request):
    imagenes = Imagen.objects.all()  # Obtiene todas las imágenes de la base de datos

    if request.method == 'POST':  # Verifica si la solicitud es de tipo POST
        imagen_id = request.POST.get('imagen_id')  # Obtiene el ID de la imagen (si se está editando)
        imagen = Imagen.objects.get(id=imagen_id) if imagen_id else None

        if imagen:  # Si la imagen existe
            form = ImagenForm(request.POST, request.FILES, instance=imagen)
            if form.is_valid():
                form.save()  # Guarda los cambios realizados en la imagen
                return redirect('cargar_imagenes')
    else:
        # Si la solicitud no es POST, muestra un formulario vacío
        form = ImagenForm()

    # Renderiza la vista para cargar o editar imágenes
    return render(request, 'vistasPrivadas/cargar_imagenes.html', {'form': form, 'imagenes': imagenes})






























































































"""def imprimir_datos_por_documento(request, documento):
    # Obtener la persona por documento
    persona = get_object_or_404(Persona, documento=documento)
    trazabilidades = Trazabilidad.objects.filter(persona=persona)

    # Imprimir en la consola los datos
    print(f"Nombre: {persona.nombre}")
    print(f"Documento: {persona.documento}")
    print(f"Programa: {persona.programa}")
    print(f"Fecha de Grado: {persona.fechagrado}")

    print("\nTrazabilidades:")
    for trazabilidad in trazabilidades:
        print(f"Ubicación Laboral: {trazabilidad.ubicacion_laboral}")
        print(f"Correo Electrónico: {trazabilidad.correoelectronico}")
        print(f"Teléfono: {trazabilidad.telefono}")
        print(f"Oferta: {trazabilidad.oferta}")
        print(f"Fecha de Modificación: {trazabilidad.fecha_modificacion}")
        print("-" * 50)

    # Retornar una respuesta HTTP sencilla
    return HttpResponse("Datos impresos en la consola correctamente.")"""
    