# Importamos las bibliotecas necesarias para la configuración de URLs de Django.
from django.contrib import admin
from django.urls import path
from login import views  # Importamos las vistas de la app 'login' para usarlas en las rutas.
from django.conf import settings
from django.conf.urls.static import static  # Importamos para manejar archivos estáticos y de medios.

# Definimos las URLs de nuestra aplicación en la lista 'urlpatterns'.
urlpatterns = [
    # Ruta para el panel de administración de Django.
    path('admin/', admin.site.urls),  # Acceso al panel de administración de Django.
    # Ruta para la página de inicio ('home'). Esta es la página principal.
    path('', views.home, name='home'),
    # Ruta que permite acceder a la página de inicio con un segmento adicional en la URL.
    path('home/<path:extra>/', views.home),
    # Rutas para el registro de usuarios.
    path('signup/', views.signup, name='signup'),  # Ruta para registrarse.
    path('signup/<path:extra>/', views.signup),  # Ruta para registrarse con un segmento adicional.
    # Rutas para la página privada, accesible solo por usuarios logueados.
    path('private/', views.private, name='private'),  # Ruta para la página privada.
    path('private/<path:extra>/', views.private),  # Ruta para la página privada con un segmento adicional.
    # Ruta para cerrar sesión.
    path('signout/', views.signout, name='logout'),  # Ruta para cerrar sesión.
    path('signout/<path:extra>/', views.signout),  # Ruta para cerrar sesión con un segmento adicional.
    # Rutas para iniciar sesión.
    path('signin/', views.signin, name='signin'),  # Ruta para iniciar sesión.
    path('signin/<path:extra>/', views.signin),  # Ruta para iniciar sesión con un segmento adicional.
    # Ruta para cargar archivos (en este caso, archivos CSV).
    path('cargar/', views.cargar_archivo, name='cargar_archivo'),  # Ruta para cargar archivos.
    path('cargar/<path:extra>/', views.cargar_archivo),  # Ruta para cargar archivos con un segmento adicional.
    # Ruta para guardar los datos provenientes de un archivo.
    path('guardar_datos/', views.guardar_datos, name='guardar_datos'),  # Ruta para guardar los datos procesados.
    # Ruta para mostrar un mensaje de éxito después de guardar los datos.
    path('exito_guardado/', views.exito_guardado, name='exito_guardado'),
    # Ruta para buscar personas por su documento.
    path('buscarpersona/', views.buscar, name='buscar'),  # Ruta para buscar personas.
    # Ruta para ver el detalle de una persona, identificada por su documento.
    path('persona/<str:documento>/', views.detalle_persona, name='buscar_resultado'),
    # Ruta para ver la trazabilidad de una persona, identificada por su documento.
    path('persona/trazabilidad/<str:documento>/', views.ver_trazabilidad, name='ver_trazabilidad'),
    # Ruta para agregar trazabilidad a una persona.
    path('persona/<str:documento>/agregar_trazabilidad/', views.agregar_trazabilidad, name='agregar_trazabilidad'),
    # Ruta para modificar trazabilidad de una persona, identificada por el ID de la trazabilidad.
    path('trazabilidad/modificar/<int:trazabilidad_id>/', views.modificar_trazabilidad, name='modificar_trazabilidad'),
    # Ruta para eliminar una trazabilidad de una persona, identificada por el ID de la trazabilidad.
    path('trazabilidad/eliminar/<int:trazabilidad_id>/', views.eliminar_trazabilidad, name='eliminar_trazabilidad'),
    # Rutas para manejar los egresados destacados.
    path('egresadosDestacados/', views.egresadosDestacados, name="egresadosDestacados"),  # Ruta para ver los egresados destacados.
    # Ruta para editar un egresado destacado, identificado por su ID.
    path('editar/<int:id>/', views.editar_egresado, name='editar_egresado'),
    # Ruta para listar todos los egresados destacados.
    path('egresados-destacados/', views.listar_egresados_destacados, name='listar_egresados_destacados'),
    # Ruta para ver el detalle de un egresado destacado, identificado por su ID.
    path('egresado/<int:egresado_id>/', views.egresado_detalle, name='egresado_detalle'),

    # Ruta para cargar imágenes en la base de datos.
    path('cargar-imagenes/', views.cargar_imagenes, name='cargar_imagenes')
]

# Si estamos en modo de desarrollo (DEBUG = True), configuramos la ruta para los archivos estáticos.
if settings.DEBUG:
    # Sirve los archivos estáticos (por ejemplo, imágenes o archivos de medios) en el desarrollo.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
