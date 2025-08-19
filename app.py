from datetime import datetime

from flask import Flask, render_template, request, abort

app = Flask(__name__)

PAGES = {
    'trabajos',
    'cucha',
    'articulos',
    'sintesis',
    'sobre_mi',
    'contacto',
    'cv'
}


# Lista de trabajos para mostrar automáticamente los más recientes
TRABAJOS = [
    {
        "titulo": "Análisis Avanzado en Excel – Proyecto Final",
        "descripcion": "Dashboard interactivo sobre contenido y métricas.",
        "link": "docs/ProyectoFinal_Bonacci_Santiago.xlsx",
        "externo": False,
        "fecha": datetime(2025, 3, 1),
    },
    {
        "titulo": "Informe Estratégico sobre Rendimiento en Instagram",
        "descripcion": "Informe de métricas clave y recomendaciones.",
        "link": "docs/Métricas Cuchá 23-25.pdf",
        "externo": False,
        "fecha": datetime(2025, 2, 15),
    },
    {
        "titulo": "Automatización con Python + IA",
        "descripcion": "Script que resume PDFs y genera copies para redes.",
        "link": "https://github.com/sbonacci33/TuPrimeraPagina-Bonacci",
        "externo": True,
        "fecha": datetime(2025, 1, 10),
    },
    {
        "titulo": "Síntesis Estratégica — Proyecto Web con Django",
        "descripcion": "Plataforma web que integra análisis y comunicación.",
        "link": "https://sintesisestrategica.onrender.com/",
        "externo": True,
        "fecha": datetime(2024, 12, 1),
    },
]


@app.route('/')
def index():
    trabajos_recientes = sorted(TRABAJOS, key=lambda x: x["fecha"], reverse=True)[:3]
    return render_template('index.html', trabajos_recientes=trabajos_recientes)

@app.route('/<page>')
def render_page(page: str):
    if page in PAGES:
        return render_template(f"{page}.html")
    abort(404)

# Context processor para usar `request.endpoint` en templates
@app.context_processor
def inject_request():
    return dict(request=request)

# Ejecución de la app
if __name__ == '__main__':
    app.run(debug=True)
