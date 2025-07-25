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
    
# Datos temporales (simulación)
bancos_data = {
    "venezuela": [],
    "peru": [],
    "chile": [],
    "colombia": []
}

# Página HTML
@app.route('/bancos/<pais>')
def mostrar_bancos(pais):
    return render_template('bancos.html', pais=pais)

@app.route('/bancos/<pais>')
def bancos(pais):
    if pais not in bancos_data:
        return "País no válido", 404
    return render_template('bancos.html', pais=pais)

# API para gestionar bancos
@app.route('/api/bancos/<pais>', methods=['GET'])
def api_get_bancos(pais):
    return jsonify(bancos_data.get(pais, []))

@app.route('/api/bancos/<pais>', methods=['POST'])
def api_add_banco(pais):
    nombre = request.json.get('nombre')
    if pais in bancos_data and nombre:
        bancos_data[pais].append(nombre)
    return jsonify(success=True)

@app.route('/api/bancos/<pais>/<int:index>', methods=['DELETE'])
def api_delete_banco(pais, index):
    if pais in bancos_data and 0 <= index < len(bancos_data[pais]):
        bancos_data[pais].pop(index)
    return jsonify(success=True)

@app.route('/api/bancos/<pais>/<int:index>', methods=['PUT'])
def api_edit_banco(pais, index):
    nuevo_nombre = request.json.get('nombre')
    if pais in bancos_data and 0 <= index < len(bancos_data[pais]):
        bancos_data[pais][index] = nuevo_nombre
    return jsonify(success=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
