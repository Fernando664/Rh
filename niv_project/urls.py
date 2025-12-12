"""
URL configuration for niv_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from pathlib import Path
from django.shortcuts import render
from materias.models import Materia  # ✅ CORRECTO

BASE_DIR = Path(__file__).resolve().parent.parent

def index(request):
    
    # Si el usuario envía el formulario
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        semestre = request.POST.get('semestre', '').strip()
        profesor = request.POST.get('profesor', '').strip()
        comentarios = request.POST.get('comentarios', '').strip()
        
        if nombre and semestre and profesor:
            # Crear una nueva materia en la base de datos
            Materia.objects.create(nombre=nombre, semestre=semestre, profesor=profesor, comentarios=comentarios)
    
    # Obtener todas las materias
    materias = Materia.objects.all().order_by('-fecha')
    
    # Pasar datos al template
    context = {
        'materias': materias,
        'materias_count': materias.count(),
        'semesters': range(1, 13)
    }
    
    return render(request, 'index.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
]
