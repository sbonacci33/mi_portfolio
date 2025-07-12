# Portfolio profesional con Flask

Este proyecto es una web personal creada con **Flask** que muestra mis trabajos y experiencia profesional. Utiliza plantillas HTML con **Jinja**, estilos en **CSS** y componentes de **Bootstrap** para lograr un diseño responsivo.

## Instalación local

1. Clona este repositorio.
2. Crea un entorno virtual en Python e instala las dependencias:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación:
   ```bash
   python app.py
   ```
4. Abre `http://127.0.0.1:5000` en tu navegador para ver la página.

## Tecnologías usadas
- **Flask** como framework web.
- **HTML**, **CSS** y **Jinja2** para las plantillas.
- **Bootstrap** para el diseño responsivo.

## Despliegue en PythonAnywhere

1. Crea una cuenta en [PythonAnywhere](https://www.pythonanywhere.com/).
2. Sube el código del proyecto (puedes usar GitHub y clonar el repositorio desde la consola de PythonAnywhere).
3. En la sección *Web* de PythonAnywhere crea una nueva aplicación Flask apuntando al archivo `app.py`.
4. Instala las dependencias dentro del entorno virtual de PythonAnywhere usando `pip install -r requirements.txt`.
5. Reinicia la aplicación desde el panel y accede a tu dominio asignado.

