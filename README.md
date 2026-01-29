Desarrollo de un Gestor de Tareas con metodología Scrum

## Descripción
El proyecto tiene como objetivo desarrollar una aplicación Web sencilla para gestionar tareas, aplicar reglas de negocio realistas y realizar trabajos siguiendo la metodología de Scrum. Las tareas se almacenan en una estructura de datos en el backend la cual permanece activa mientras el servidor esté en ejecución. En este sprint se implementa la persistencia en memoria para validar la lógica del backend antes de integrar una base de datos en sprints posteriores. Actualmente la aplicación está pensada para ejecutarse en local. Cada usuario puede clonar el repositorio, arrancar el backend y usar el gestor de tareas en su propio equipo. Para un entorno real, sería necesario desplegar el backend en un servidor y usar una base de datos para compartir las tareas entre usuarios.

Instrucciones:
1. Definir o crear tarea
2. Modificar proridades o solicitar cambios en el producto
3. Repartir roles
4. Establecer en qué fase se encuentra la tarea 

Funcionalidades implementadas:
1. Añadir etiquetas
2. Organizar tareas
3. Asignación y modificación de roles

## Persistencia básica de datos
1. Al iniciar el backend se crea una lista de tareas en memoria
2. Las peticiones GET devuelven el contenido actual de dicha lista
3. Las peticiones POST añaden nuevas tareas a la lista
4. Al reiniciar el sistema las tareas se pierden

Esto permite simplificar el desarrollo inicial, centrarse en la base del sistema y la comunicación frontend-backend.

Integrantes:
Mónica Berenice Paulín López | A01707696  
Sofía Cabáñez de la Peña | A01707231 
Natalia Esteves Ríos | A01705453 
Claudia Rebeca Guatemala Gómez |A01705453
Irán Carmona Díaz |A01709666
