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

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


# ---- NUEVO: Configuración de Base de Datos y CRUD Bancos ----
import sqlite3
from flask import request, jsonify

DB_NAME = 'cambio_express.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bancos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        pais TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.before_first_request
def initialize():
    init_db()

# API para Bancos
@app.route('/api/bancos/<pais>', methods=['GET'])
def listar_bancos(pais):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, nombre FROM bancos WHERE pais=?", (pais.capitalize(),))
    bancos = [{"id": row[0], "nombre": row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(bancos)

@app.route('/api/bancos', methods=['POST'])
def agregar_banco():
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO bancos (nombre, pais) VALUES (?, ?)", (data['nombre'], data['pais']))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route('/api/bancos/<int:id>', methods=['PUT'])
def editar_banco(id):
    data = request.json
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE bancos SET nombre=? WHERE id=?", (data['nombre'], id))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route('/api/bancos/<int:id>', methods=['DELETE'])
def eliminar_banco(id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM bancos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})
