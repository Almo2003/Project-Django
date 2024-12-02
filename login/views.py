from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, Http404
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import csv
from .forms import CSVUploadForm, TrazabilidadForm, EgresadoForm
import pandas as pd
import io
from .models import Persona, Trazabilidad, Egresado
import json
from django.core.files.storage import FileSystemStorage

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

@login_required    
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

@login_required

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
            documento = row[1] if len(row) > 1 else None
            programa = row[2] if len(row) > 2 else None
            fechagrado = row[3] if len(row) > 3 else None
            ubicacion_laboral = row[4] if len(row) > 4 else None
            correoelectronico = row[5] if len(row) > 5 else None
            telefono = row[6] if len(row) > 6 else None
            oferta = row[7] if len(row) > 7 else None

            # Verificar si ya existe un registro con el mismo documento
            if documento and not Persona.objects.filter(documento=documento).exists():
                try:
                    # Crear y guardar una nueva instancia de Persona
                    persona = Persona(
                        nombre=nombre,
                        documento=documento,
                        programa=programa,
                        fechagrado=fechagrado
                    )
                    persona.save()

                    # Crear la instancia de Trazabilidad para los campos dinámicos
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
                print(f"Registro duplicado encontrado para documento: {documento}")

        # Mostrar un mensaje de éxito
        return redirect('exito_guardado')

    return redirect('cargar_archivo')


def exito_guardado(request):
    return render(request, 'exito_guardado.html')

@login_required
def buscar(request):
    if request.method == 'POST':
        documento = request.POST.get('documento')  # Obtenemos el documento del formulario

        try:
            persona = Persona.objects.get(documento=documento)  # Intentamos obtener la persona

            # Obtener la trazabilidad asociada a esta persona (si existe)
            trazabilidades = Trazabilidad.objects.filter(persona=persona)  # Asumiendo que 'Persona' tiene una relación con 'Trazabilidad'

            return render(request, './vistasPrivadas/buscar_resultado.html', {
                'persona': persona,
                'trazabilidades': trazabilidades,
            })
        except Persona.DoesNotExist:
            # Si no existe, mostramos un mensaje de error
            error_message = f"No se encontró ninguna persona con el documento {documento}."
            return render(request, './vistasPrivadas/buscarpersona.html', {'error_message': error_message})

    return render(request, './vistasPrivadas/buscarpersona.html')


@login_required
def ver_trazabilidad(request, documento):
    persona = get_object_or_404(Persona, documento=documento)
    trazabilidades = persona.trazabilidades.all()  # Obtiene el historial de trazabilidad de la persona
    context = {
        'persona': persona,
        'trazabilidades': trazabilidades,
    }
    return render(request, './vistasPrivadas/ver_trazabilidad.html', context)

@login_required
def detalle_persona(request, documento):
    # Busca la persona por su documento
    persona = get_object_or_404(Persona, documento=documento)
    
    # Obtén la trazabilidad asociada a la persona
    trazabilidades = Trazabilidad.objects.filter(persona=persona)
    contexto = {
        'persona': persona,
        'trazabilidades': trazabilidades,
    }
    
    return render(request, './vistasPrivadas/buscar_resultado.html', contexto)

@login_required
def agregar_trazabilidad(request, documento):
    persona = get_object_or_404(Persona, documento=documento)

    if request.method == 'POST':
        form = TrazabilidadForm(request.POST)
        if form.is_valid():
            # Crear y guardar la nueva trazabilidad
            Trazabilidad.objects.create(
                persona=persona,
                ubicacion_laboral=form.cleaned_data['ubicacion_laboral'],
                correoelectronico=form.cleaned_data['correoelectronico'],
                telefono=form.cleaned_data['telefono'],
                oferta=form.cleaned_data['oferta'],
            )                  # Guarda la trazabilidad
            return redirect('buscar_resultado', documento=documento)  # Redirige al detalle de la persona
    else:
        form = TrazabilidadForm()

    return render(request, './vistasPrivadas/agregar_trazabilidad.html', {'form': form, 'persona': persona})

@login_required
def modificar_trazabilidad(request, trazabilidad_id):
    trazabilidad = get_object_or_404(Trazabilidad, id=trazabilidad_id)
    
    if request.method == 'POST':
        form = TrazabilidadForm(request.POST, instance=trazabilidad)
        if form.is_valid():
            form.save()
            return redirect('ver_trazabilidad', documento=trazabilidad.persona.documento)  # Redirige a la vista de trazabilidad
    else:
        form = TrazabilidadForm(instance=trazabilidad)
    
    return render(request, './vistasPrivadas/agregar_trazabilidad.html', {'form': form, 'persona': trazabilidad.persona})


@login_required
def eliminar_trazabilidad(request, trazabilidad_id):
    trazabilidad = get_object_or_404(Trazabilidad, id=trazabilidad_id)
    documento = trazabilidad.persona.documento  # Para redirigir después
    trazabilidad.delete()  # Elimina la trazabilidad
    
    return redirect('ver_trazabilidad', documento=documento)  # Redirige a la vista de trazabilidad

def egresadosDestacados(request):
    # Lista de egresados destacados con datos estáticos
    egresados = [
        {
            'id': 1,
            'nombre': 'Juan Pérez',
            'profesion': 'Ingeniero de Sistemas',
            'anio_grado': 2015,
            'cargo_actual': 'Desarrollador Senior',
            'correo': 'juan.perez@example.com',
            'descripcion': 'Juan ha trabajado en grandes empresas de tecnología.',
            'trayectoria': ['Desarrollador Junior en TechCorp (2015-2017)', 'Líder Técnico en Innovatech (2017-2019)', 'Gerente de Proyectos en NextGen Solutions (2019-presente)'],
            'datos_adicionales': 'Certificaciones en Scrum Master y PMP. Participa en conferencias internacionales.',
            'imagen_url': 'https://www.iser.edu.co/wp-content/uploads/2023/08/WhatsApp-Image-2019-05-02-at-4.44.54-PM-1024x682.jpeg'
        },
        {
            'id': 2,
            'nombre': 'Karol Juliana Peña Vera',
            'profesion': 'Contadora Pública',
            'anio_grado': 2018,
            'cargo_actual': 'Analista Financiero',
            'correo': 'karol.peñavera@example.com',
            'descripcion': 'Karol tiene una gran experiencia en el sector financiero.',
            'trayectoria': ['Analista en FinCorp (2018-2020)', 'Gerente de Finanzas en MoneyTech (2020-presente)'],
            'datos_adicionales': 'Especialista en Finanzas Corporativas.',
            'imagen_url': 'https://yourteenmag.com/wp-content/uploads/2013/06/Depositphotos_24196475_l-2015.jpg'
        }
    ]
    
    return render(request, './vistasPrivadas/egresadosDestacados.html', {'egresados': egresados})

def editar_egresado(request, id):
    # Lista estática de egresados
    egresados = [
        {
            'id': 1,
            'nombre': 'Juan Pérez',
            'profesion': 'Ingeniero de Sistemas',
            'anio_grado': 2015,
            'cargo_actual': 'Desarrollador Senior',
            'correo': 'juan.perez@example.com',
            'descripcion': 'Juan ha trabajado en grandes empresas de tecnología.',
            'trayectoria': ['Desarrollador Junior en TechCorp (2015-2017)', 'Líder Técnico en Innovatech (2017-2019)', 'Gerente de Proyectos en NextGen Solutions (2019-presente)'],
            'datos_adicionales': 'Certificaciones en Scrum Master y PMP. Participa en conferencias internacionales.',
            'imagen_url': 'https://www.iser.edu.co/wp-content/uploads/2023/08/WhatsApp-Image-2019-05-02-at-4.44.54-PM-1024x682.jpeg'
        },
        {
            'id': 2,
            'nombre': 'Karol Juliana Peña Vera',
            'profesion': 'Contadora Pública',
            'anio_grado': 2018,
            'cargo_actual': 'Analista Financiero',
            'correo': 'karol.peñavera@example.com',
            'descripcion': 'Karol tiene una gran experiencia en el sector financiero.',
            'trayectoria': ['Analista en FinCorp (2018-2020)', 'Gerente de Finanzas en MoneyTech (2020-presente)'],
            'datos_adicionales': 'Especialista en Finanzas Corporativas.',
            'imagen_url': 'https://yourteenmag.com/wp-content/uploads/2013/06/Depositphotos_24196475_l-2015.jpg'
        }
    ]
    
    # Buscar el egresado por su ID
    egresado = next((item for item in egresados if item['id'] == id), None)
    
    if egresado is None:
        # Si no se encuentra el egresado, redirigir o mostrar un error
        return redirect('egresadosDestacados')
    
    if request.method == 'POST':
        # Si es una solicitud POST, se debe actualizar el egresado
        egresado['nombre'] = request.POST.get('nombre', egresado['nombre'])
        egresado['profesion'] = request.POST.get('profesion', egresado['profesion'])
        egresado['anio_grado'] = request.POST.get('anio_grado', egresado['anio_grado'])
        egresado['cargo_actual'] = request.POST.get('cargo_actual', egresado['cargo_actual'])
        egresado['correo'] = request.POST.get('correo', egresado['correo'])
        egresado['descripcion'] = request.POST.get('descripcion', egresado['descripcion'])
        egresado['trayectoria'] = request.POST.get('trayectoria', egresado['trayectoria']).split(', ')
        egresado['datos_adicionales'] = request.POST.get('datos_adicionales', egresado['datos_adicionales'])
        
        # Manejar la carga de la imagen
        if 'imagen' in request.FILES:
            imagen = request.FILES['imagen']
            fs = FileSystemStorage()
            filename = fs.save(imagen.name, imagen)
            egresado['imagen_url'] = fs.url(filename)
            
        # No se usa `.save()` porque no estamos trabajando con una base de datos
        # Redirigir después de guardar los cambios
        return redirect('egresadosDestacados')
    
    return render(request, './vistasPrivadas/editarEgresado.html', {'egresado': egresado})




























































































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
    