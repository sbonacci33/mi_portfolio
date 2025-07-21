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

@app.route('/')
def index():
    return render_template('index.html')

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
