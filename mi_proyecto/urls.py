from django.urls import path
import sqlite3
from pathlib import Path
from django.http import HttpResponse

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
    materias = cursor.fetchall()
    conn.close()
    
    # HTML de la página
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Registro de Materias</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: Arial, sans-serif; 
                background: #f0f0f0; 
                padding: 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 25px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #8a2be2;
                text-align: center;
                margin-bottom: 25px;
                padding-bottom: 10px;
                border-bottom: 2px solid #e6e6fa;
            }
            .formulario {
                background: #f8f8ff;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 30px;
            }
            .campo {
                margin-bottom: 15px;
            }
            label {
                display: block;
                margin-bottom: 5px;
                color: #333;
                font-weight: bold;
            }
            input, select, textarea {
                width: 100%;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
            }
            textarea {
                resize: vertical;
                min-height: 80px;
            }
            .boton {
                background: #8a2be2;
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
                margin-top: 10px;
            }
            .boton:hover {
                background: #7b1dd1;
            }
            .tabla {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            .tabla th {
                background: #8a2be2;
                color: white;
                padding: 12px;
                text-align: left;
            }
            .tabla td {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            .tabla tr:nth-child(even) {
                background: #f9f9f9;
            }
            .error {
                color: #ff4444;
                font-size: 14px;
                margin-top: 5px;
            }
            .contador {
                color: #8a2be2;
                font-weight: bold;
                margin: 15px 0;
            }
            @media (max-width: 600px) {
                .container { padding: 15px; }
                .tabla { font-size: 14px; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📚 Sistema de Materias</h1>
            
            <div class="formulario">
                <h2>Agregar Nueva Materia</h2>
                <form method="POST" onsubmit="return validarFormulario()">
                    <div class="campo">
                        <label>Nombre de la Materia *</label>
                        <input type="text" name="nombre" id="nombre" placeholder="Ej: Matemáticas">
                        <div id="errorNombre" class="error"></div>
                    </div>
                    
                    <div class="campo">
                        <label>Semestre *</label>
                        <select name="semestre" id="semestre">
                            <option value="">Selecciona el semestre</option>
    '''
    
    # Generar opciones de semestre del 1 al 12
    for i in range(1, 13):
        html += f'<option value="{i}">{i}° Semestre</option>'
    
    html += f'''
                        </select>
                        <div id="errorSemestre" class="error"></div>
                    </div>
                    
                    <div class="campo">
                        <label>Nombre del Profesor *</label>
                        <input type="text" name="profesor" id="profesor" placeholder="Ej: Dr. Pérez">
                        <div id="errorProfesor" class="error"></div>
                    </div>
                    
                    <div class="campo">
                        <label>Comentarios (opcional)</label>
                        <textarea name="comentarios" id="comentarios" placeholder="Observaciones sobre la materia..."></textarea>
                        <div id="errorComentarios" class="error"></div>
                    </div>
                    
                    <button type="submit" class="boton">Guardar Materia</button>
                </form>
            </div>
            
            <div class="contador">Total de materias registradas: {len(materias)}</div>
            
    '''
    
    if materias:
        html += '''
            <table class="tabla">
                <thead>
                    <tr>
                        <th>Materia</th>
                        <th>Semestre</th>
                        <th>Profesor</th>
                        <th>Comentarios</th>
                        <th>Fecha</th>
                    </tr>
                </thead>
                <tbody>
        '''
        
        for materia in materias:
            comentarios = materia[4] if materia[4] else "-"
            fecha = materia[5][:16] if materia[5] else "-"
            
            html += f'''
                    <tr>
                        <td>{materia[1]}</td>
                        <td>{materia[2]}°</td>
                        <td>{materia[3]}</td>
                        <td>{comentarios}</td>
                        <td>{fecha}</td>
                    </tr>
            '''
        
        html += '''
                </tbody>
            </table>
        '''
    else:
        html += '<p style="text-align: center; color: #666;">No hay materias registradas aún.</p>'
    
    html += '''
        </div>
        
        <script>
            function validarFormulario() {
                let valido = true;
                
                // Limpiar errores anteriores
                document.querySelectorAll('.error').forEach(e => e.textContent = '');
                
                // Validar nombre
                const nombre = document.getElementById('nombre').value.trim();
                if (!nombre) {
                    document.getElementById('errorNombre').textContent = 'El nombre es obligatorio';
                    valido = false;
                }
                
                // Validar semestre
                const semestre = document.getElementById('semestre').value;
                if (!semestre) {
                    document.getElementById('errorSemestre').textContent = 'Selecciona un semestre';
                    valido = false;
                }
                
                // Validar profesor
                const profesor = document.getElementById('profesor').value.trim();
                if (!profesor) {
                    document.getElementById('errorProfesor').textContent = 'El profesor es obligatorio';
                    valido = false;
                }
                
                // Validar comentarios (opcional, pero con límite)
                const comentarios = document.getElementById('comentarios').value.trim();
                if (comentarios.length > 500) {
                    document.getElementById('errorComentarios').textContent = 'Máximo 500 caracteres';
                    valido = false;
                }
                
                return valido;
            }
            
            // Limpiar errores al escribir
            ['nombre', 'semestre', 'profesor', 'comentarios'].forEach(id => {
                document.getElementById(id).addEventListener('input', function() {
                    const errorId = 'error' + id.charAt(0).toUpperCase() + id.slice(1);
                    document.getElementById(errorId).textContent = '';
                });
            });
        </script>
    </body>
    </html>
    '''
    
    return HttpResponse(html)

urlpatterns = [
    path('', index),
]