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
        "titulo": "Informe de Métricas de Instagram – T2 2025",
        "descripcion": "Diagnóstico del segundo trimestre 2025 comparado con siete previos.",
        "link": "docs/INFORME MÉTRICAS T2 CUCHÁ.pdf",
        "externo": False,
        "fecha": datetime(2025, 8, 15),
    },
    {
        "titulo": "Dashboard de Rendimiento de Contenidos en Tableau",
        "descripcion": "Evaluación de publicaciones por formato, temática y horario.",
        "link": "https://public.tableau.com/app/profile/santiago.bonacci/viz/EntregaFinalSantiagoBonacci/Inicio",
        "externo": True,
        "fecha": datetime(2025, 8, 1),
    },
    {
        "titulo": "Informe Estratégico sobre Rendimiento en Instagram",
        "descripcion": "Informe de métricas clave y recomendaciones.",
        "link": "docs/Informe Metricas Instagram Junio 2023 - Julio 2025.pdf",
        "externo": False,
        "fecha": datetime(2025, 7, 15),
    },
    {
        "titulo": "Automatización con Python + IA",
        "descripcion": "Script que resume PDFs y genera copies para redes.",
        "link": "https://github.com/sbonacci33/TuPrimeraPagina-Bonacci",
        "externo": True,
        "fecha": datetime(2025, 6, 15),
    },
    {
        "titulo": "Análisis Avanzado en Excel – Proyecto Final",
        "descripcion": "Dashboard interactivo sobre contenido y métricas.",
        "link": "docs/ProyectoFinal_Bonacci_Santiago.xlsx",
        "externo": False,
        "fecha": datetime(2025, 6, 1),
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
