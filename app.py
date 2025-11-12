from datetime import datetime
import os

from flask import Flask, render_template, request, abort

app = Flask(__name__)
app.config['GA4_ID'] = os.environ.get('GA4_ID')  # ej. "G-XXXXXXXXXX" o None

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


@app.route("/trabajos/analisis/balance-tiktok-instagram")
def balance_tiktok_instagram():
    description = (
        "Análisis del período noviembre 2024 – octubre 2025 de cuenta, donde se evalúan las principales métricas y características "
        "de seguidores para balance, síntesis y nueva estrategia digital."
    )
    return render_template(
        "trabajos/analisis/balance-tiktok-instagram.html",
        page_title="Resumen de Informe anual de TikTok e Instagram | Santiago Bonacci",
        page_description=description,
        og_title="Resumen de Informe anual de TikTok e Instagram",
        og_description=description,
        twitter_title="Resumen de Informe anual de TikTok e Instagram",
        twitter_description=description,
    )

# Context processor para usar `request.endpoint` en templates
@app.context_processor
def inject_request():
    return dict(request=request)


@app.context_processor
def inject_ga4():
    return {'GA4_ID': app.config.get('GA4_ID')}


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

# Ejecución de la app
if __name__ == '__main__':
    app.run(debug=True)
