# MHApp
Aplicación desarrollada en Python usando la librería Tkinter para la GUI y con una BBDD SQL.
Esta herramienta unifica distintas tareas de pentesting, tanto de análisis de vulnerabilidades como de OSINT.
#### Funcionalidades implementadas
Ejecución de la herramienta Nmap con distintas variantes.
Ejecución de Curl.
Automatización de búsquedas usando Google Dorks.
Geolocalización de Ip's.

## Fallos
### Estilo del NoteBook en el Main_Window
Se puede cambiar el estilo de toda la aplicación importando el archivo App_Styles, pero dicho estilo no se aplica en el Notebook creado en la ventana Main_Window ni en las pestañas del mismo.
### Control de los mensajes de error
Controlar todos los mensajes de error para que aparezcan en la interfaz y no por consola.


## Cosas a implementar
### Mejoras en la seguridad
Implementar una autenticación de doble factor y comprobar la seguridad de la encriptación utilizada.
### Integración con API de terceros
Añadir integración de alguna API externa para el envío de informes directamente a emails de usuarios.
### Generador de informes
Usando la libería Canva (o la más eficiente) integrar la funcionalidad de generar, maquetar y descargar informes.
### Implementación de la funcionalidad "Social Media"
A través de la librería Request poder obtener información de usuarios en distintas RRSS usando el email.
### Refactorización de código
Revisión general de todo el código, pero centrándose en el Main_Window y la generación dinámica de pestañas a partir de imports dinámicos.
