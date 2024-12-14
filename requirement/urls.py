"""
URL configuration for requirement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('home/<path:extra>/', views.home),
    path('signup/', views.signup, name='signup'),
    path('signup/<path:extra>/', views.signup),
    path('private/', views.private, name='private'),
    path('private/<path:extra>/', views.private),
    path('signout/', views.signout, name='logout'),
    path('signout/<path:extra>/', views.signout),
    path('signin/', views.signin, name='signin'),
    path('signin/<path:extra>/', views.signin),
    path('cargar/', views.cargar_archivo, name='cargar_archivo'),
    path('cargar/<path:extra>/', views.cargar_archivo),
    path('guardar_datos/', views.guardar_datos, name='guardar_datos'),
    path('exito_guardado/', views.exito_guardado, name='exito_guardado'),
    path('buscarpersona/', views.buscar, name='buscar'),
    path('persona/<str:documento>/', views.detalle_persona, name='buscar_resultado'),
    path('persona/trazabilidad/<str:documento>/', views.ver_trazabilidad, name='ver_trazabilidad'),
    path('persona/<str:documento>/agregar_trazabilidad/', views.agregar_trazabilidad, name='agregar_trazabilidad'),
    path('trazabilidad/modificar/<int:trazabilidad_id>/', views.modificar_trazabilidad, name='modificar_trazabilidad'),
    path('trazabilidad/eliminar/<int:trazabilidad_id>/', views.eliminar_trazabilidad, name='eliminar_trazabilidad'),
    path('egresadosDestacados/', views.egresadosDestacados, name="egresadosDestacados" ),
    path('editar/<int:id>/', views.editar_egresado, name='editar_egresado'),
    path('egresados-destacados/', views.listar_egresados_destacados, name='listar_egresados_destacados'),
    path('egresado/<int:egresado_id>/', views.egresado_detalle, name='egresado_detalle'),
    path('cargar-imagenes/', views.cargar_imagenes, name='cargar_imagenes')

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
