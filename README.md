Desarrollo de un Gestor de Tareas con metodología Scrum

Integrantes:
Mónica Berenice Paulín López | A01707696  
Sofía Cabáñez de la Peña | A01707231 
Natalia Esteves Ríos | A01705453 
Claudia Rebeca Guatemala Gómez |A01705453
Irán Carmona Díaz |A01709666

## Descripción
Aplicación web para gestión de tareas implementando metodología Scrum con tablero Kanban.

## Instalación y Ejecución
1. Clonar repositorio
```bash
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_CARPETA]

2.⁠ ⁠Instalar dependencias
pip install flask flask-cors

3.⁠ ⁠Para ejecutar servidor
python app.py

4.⁠ ⁠Acceder a la aplicación
Servidor backend: http://localhost:5000
Interfaz web: Abrir index.html en navegador
API Endpoints: Ver sección siguiente

**## API Endpoints**
Método	Endpoint	Descripción
GET	/	Estado del servidor
GET	/tasks	Obtener todas las tareas
POST	/tasks	Crear nueva tarea
PUT	/tasks/{id}	Actualizar tarea
DELETE	/tasks/{id}	Eliminar tarea
GET	/users	Obtener todos los usuarios
POST	/users	Crear nuevo usuario
PUT	/users/{id}	Actualizar usuario
DELETE	/users/{id}	Eliminar usuario
GET	/stats	Obtener estadísticas

Límite en Doing: Máximo 4 tareas en columna "Doing"

Validación usuarios: No puede haber usuarios duplicados

Desasignación automática: Al eliminar usuario, sus tareas quedan sin asignar

Tiempo real: Solo se puede ingresar en columna "Done"

Validaciones: Título obligatorio, IDs válidos


Características
- CRUD completo de tareas y usuarios
- Tablero Kanban con 3 columnas (Backlog, Doing, Done)
- Gestión de usuarios con asignación de tareas
- Validaciones de negocio (máximo 4 tareas en Doing)
- Estadísticas en tiempo real
- Drag & Drop entre columnas
- Persistencia en JSON (sin base de datos)

Tecnologías
- Backend: Python + Flask
- Frontend: HTML5, CSS3, JavaScript Vanilla
- Persistencia: JSON files
- CORS: Flask-CORS

Requisitos Previos
- ⁠Python 3.8+
- pip (gestor de paquetes de Python)


