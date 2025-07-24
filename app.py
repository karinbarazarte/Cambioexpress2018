from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Dashboard funcionando en Render</h1>"

@app.route('/remesas')
def remesas():
    return "<h2>Página de Remesas funcionando</h2>"

@app.route('/bancos')
def bancos():
    return "<h2>Módulo de Bancos funcionando</h2>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
