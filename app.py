"""Aplicación Flask para el portafolio de Santiago Bonacci."""

from datetime import datetime
import os
from typing import Iterable, TypedDict

from flask import Flask, render_template, request, abort


class Trabajo(TypedDict):
    titulo: str
    descripcion: str
    link: str
    endpoint: str | None
    externo: bool
    fecha: datetime


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


BALANCE_TIKTOK_DESCRIPTION = (
    "Análisis del período noviembre 2024 – octubre 2025 de cuenta, donde se evalúan las principales métricas y características "
    "de seguidores para balance, síntesis y nueva estrategia digital."
)


# Lista de trabajos para mostrar automáticamente los más recientes
TRABAJOS: list[Trabajo] = [
    {
        "titulo": "Entrega Final SQL – Coderhouse",
        "descripcion": "Proyecto final del curso de SQL aprobado con nota 10. Diseño de base de datos relacional, consultas complejas, joins, subconsultas y vistas aplicadas a un caso real.",
        "link": "https://drive.google.com/drive/folders/1tCSmsCo0TYI1BB0lcCeOBF3QC8jn2wBp?usp=drive_link",
        "endpoint": None,
        "externo": True,
        "fecha": datetime(2026, 4, 1),
    },
    {
        "titulo": "Reporte de ventas en Power BI",
        "descripcion": "Proyecto final con reporte interactivo y modelo de datos.",
        "link": "https://drive.google.com/file/d/1qG3JHPBuQopXvYI9t9dJHLuUqY795Cds/view",
        "endpoint": None,
        "externo": True,
        "fecha": datetime(2025, 12, 15),
    },
    {
        "titulo": "Resumen de Informe anual de TikTok e Instagram",
        "descripcion": "Balance del período noviembre 2024 – octubre 2025 con métricas y aprendizajes clave.",
        "link": "docs/Balance anual TikTok Instagram.pdf",
        "endpoint": None,
        "externo": False,
        "fecha": datetime(2025, 11, 30),
    },
    {
        "titulo": "Informe de Métricas de Instagram – T2 2025",
        "descripcion": "Diagnóstico del segundo trimestre 2025 comparado con siete previos.",
        "link": "docs/INFORME MÉTRICAS T2 CUCHÁ.pdf",
        "endpoint": None,
        "externo": False,
        "fecha": datetime(2025, 8, 15),
    },
    {
        "titulo": "Dashboard de Rendimiento de Contenidos en Tableau",
        "descripcion": "Evaluación de publicaciones por formato, temática y horario.",
        "link": "https://public.tableau.com/app/profile/santiago.bonacci/viz/EntregaFinalSantiagoBonacci/Inicio",
        "endpoint": None,
        "externo": True,
        "fecha": datetime(2025, 8, 1),
    },
    {
        "titulo": "Informe Estratégico sobre Rendimiento en Instagram",
        "descripcion": "Informe de métricas clave y recomendaciones.",
        "link": "docs/Informe Metricas Instagram Junio 2023 - Julio 2025.pdf",
        "endpoint": None,
        "externo": False,
        "fecha": datetime(2025, 7, 15),
    },
    {
        "titulo": "Automatización con Python + IA",
        "descripcion": "Script que resume PDFs y genera copies para redes.",
        "link": "https://github.com/sbonacci33/TuPrimeraPagina-Bonacci",
        "endpoint": None,
        "externo": True,
        "fecha": datetime(2025, 6, 15),
    },
    {
        "titulo": "Análisis Avanzado en Excel – Proyecto Final",
        "descripcion": "Dashboard interactivo sobre contenido y métricas.",
        "link": "docs/ProyectoFinal_Bonacci_Santiago.xlsx",
        "endpoint": None,
        "externo": False,
        "fecha": datetime(2025, 6, 1),
    },
]


def _ordenar_trabajos(trabajos: Iterable[Trabajo]) -> list[Trabajo]:
    """Devuelve los trabajos ordenados por fecha descendente."""

    return sorted(trabajos, key=lambda trabajo: trabajo["fecha"], reverse=True)


TRABAJOS_ORDENADOS = _ordenar_trabajos(TRABAJOS)


@app.route('/')
def index():
    trabajos_recientes = TRABAJOS_ORDENADOS[:3]
    return render_template('index.html', trabajos_recientes=trabajos_recientes)


@app.route('/<page>')
def render_page(page: str):
    if page in PAGES:
        return render_template(f"{page}.html")
    abort(404)


@app.route("/trabajos/analisis/balance-tiktok-instagram")
def balance_tiktok_instagram():
    return render_template(
        "trabajos/analisis/balance-tiktok-instagram.html",
        page_title="Resumen de Informe anual de TikTok e Instagram | Santiago Bonacci",
        page_description=BALANCE_TIKTOK_DESCRIPTION,
        og_title="Resumen de Informe anual de TikTok e Instagram",
        og_description=BALANCE_TIKTOK_DESCRIPTION,
        twitter_title="Resumen de Informe anual de TikTok e Instagram",
        twitter_description=BALANCE_TIKTOK_DESCRIPTION,
    )


# Context processors
@app.context_processor
def inject_globals():
    return {
        "request": request,
        "GA4_ID": app.config.get("GA4_ID"),
    }


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


# Ejecución de la app
if __name__ == '__main__':
    app.run(debug=True)
