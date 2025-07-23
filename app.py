
from flask import Flask, render_template, request
import os

app = Flask(__name__)

tasas = {
    ("Perú", "Venezuela"): 3.5,
    ("Venezuela", "Perú"): 4.1,
    ("Chile", "Venezuela"): 3.2,
    ("Venezuela", "Chile"): 3.9,
    ("Perú", "Colombia"): 2.5,
    ("Perú", "Chile"): 3.0,
    ("Chile", "Perú"): 3.8,
    ("Chile", "Colombia"): 2.7,
    ("Colombia", "Chile"): 3.3,
    ("Colombia", "Perú"): 3.4,
    ("Colombia", "Venezuela"): 2.9
}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/remesas')
def remesas():
    paises = list(set([p[0] for p in tasas.keys()] + [p[1] for p in tasas.keys()]))
    bancos = ["BCP", "Interbank", "Banesco", "Banco de Venezuela", "Scotiabank"]
    colaboradores = ["María", "Pedro", "Luisa"]
    return render_template('remesas.html', paises=paises, bancos=bancos, colaboradores=colaboradores)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
