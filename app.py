from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Datos temporales en memoria
tasas = {}
paises = ["Perú", "Venezuela", "Chile", "Colombia"]
bancos = ["BCP", "Interbank", "Banesco", "Banco de Venezuela", "Scotiabank"]
colaboradores = ["María", "Pedro", "Luisa"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remesas')
def remesas():
    return render_template('remesas.html', paises=paises, bancos=bancos, colaboradores=colaboradores)

@app.route('/tasas')
def gestionar_tasas():
    return render_template('tasas.html', paises=paises, tasas=tasas)

@app.route('/agregar_tasa', methods=['POST'])
def agregar_tasa():
    origen = request.form.get('origen')
    destino = request.form.get('destino')
    valor = request.form.get('tasa')
    if origen and destino and valor:
        tasas[(origen, destino)] = float(valor)
    return jsonify(success=True, tasas=tasas)

@app.route('/eliminar_tasa', methods=['POST'])
def eliminar_tasa():
    origen = request.form.get('origen')
    destino = request.form.get('destino')
    if (origen, destino) in tasas:
        del tasas[(origen, destino)]
    return jsonify(success=True, tasas=tasas)

@app.route('/obtener_tasa', methods=['GET'])
def obtener_tasa():
    origen = request.args.get('origen')
    destino = request.args.get('destino')
    if (origen, destino) in tasas:
        return jsonify(tasa=tasas[(origen, destino)])
    return jsonify(tasa=None)
    
# Lista temporal para almacenar bancos por país
bancos_data = {
    "venezuela": [],
    "peru": [],
    "chile": [],
    "colombia": []
}

@app.route('/bancos/<pais>', methods=['GET', 'POST'])
def bancos(pais):
    if request.method == 'POST':
        banco = request.form.get('banco')
        if banco and banco not in bancos_data[pais]:
            bancos_data[pais].append(banco)
    return render_template('bancos.html', pais=pais, bancos=bancos_data[pais])

@app.route('/bancos/<pais>/eliminar/<nombre>', methods=['GET'])
def eliminar_banco(pais, nombre):
    if nombre in bancos_data[pais]:
        bancos_data[pais].remove(nombre)
    return redirect(url_for('bancos', pais=pais))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
