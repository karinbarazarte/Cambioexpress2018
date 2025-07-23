
from flask import Flask, render_template, request
import os

app = Flask(__name__)
remesas = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        cliente = request.form['cliente']
        origen = request.form['origen']
        destino = request.form['destino']
        monto = float(request.form['monto'])
        tasa = float(request.form['tasa'])
        recibido = round(monto * tasa, 2)
        nota = request.form.get('nota', '')
        remesas.append({
            'cliente': cliente,
            'origen': origen,
            'destino': destino,
            'monto': monto,
            'tasa': tasa,
            'recibido': recibido,
            'nota': nota
        })
    return render_template('dashboard.html', remesas=remesas)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
