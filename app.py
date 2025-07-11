from flask import Flask, render_template, request

app = Flask(__name__)

# Rutas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proyectos')
def proyectos():
    return render_template('proyectos.html')

@app.route('/cucha')
def cucha():
    return render_template('cucha.html')

@app.route('/articulos')
def articulos():
    return render_template('articulos.html')

@app.route('/sintesis')
def sintesis():
    return render_template('sintesis.html')

@app.route('/sobre_mi')
def sobre_mi():
    return render_template('sobre_mi.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

# Context processor para usar `request.endpoint` en templates
@app.context_processor
def inject_request():
    return dict(request=request)

# Ejecución de la app
if __name__ == '__main__':
    app.run(debug=True)
