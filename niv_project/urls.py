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
import sqlite3
from pathlib import Path
from django.shortcuts import render

BASE_DIR = Path(__file__).resolve().parent.parent

def crear_tabla():
    """Crea la tabla de materias si no existe"""
    ruta_db = BASE_DIR / 'db.sqlite3'
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            semestre INTEGER NOT NULL,
            profesor TEXT NOT NULL,
            comentarios TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def index(request):
    """Página principal con formulario y lista"""
    crear_tabla()
    
    # Si el usuario envía el formulario
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        semestre = request.POST.get('semestre', '').strip()
        profesor = request.POST.get('profesor', '').strip()
        comentarios = request.POST.get('comentarios', '').strip()
        
        if nombre and semestre and profesor:
            conn = sqlite3.connect(BASE_DIR / 'db.sqlite3')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO materias (nombre, semestre, profesor, comentarios)
                VALUES (?, ?, ?, ?)
            ''', (nombre, semestre, profesor, comentarios))
            conn.commit()
            conn.close()
    
    # Obtener todas las materias
    conn = sqlite3.connect(BASE_DIR / 'db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM materias ORDER BY fecha DESC')
    materias_data = cursor.fetchall()
    conn.close()
    
    # Convertir tuplas a diccionarios para mejor manejo en el template
    materias = []
    for materia in materias_data:
        materias.append({
            'id': materia[0],
            'nombre': materia[1],
            'semestre': materia[2],
            'profesor': materia[3],
            'comentarios': materia[4],
            'fecha': materia[5]
        })
    
    # Pasar datos al template
    context = {
        'materias': materias,
        'materias_count': len(materias),
        'semesters': range(1, 13)
    }
    
    return render(request, 'index.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
]
