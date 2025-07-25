from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

DB_NAME = 'cambio_express.db'
initialized = False

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bancos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        pais TEXT NOT NULL)''')
    conn.commit()
    conn.close()

@app.before_request
def initialize():
    global initialized
    if not initialized:
        init_db()
        initialized = True

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/remesas')
def remesas():
    return render_template('remesas.html')

@app.route('/bancos/<pais>')
def bancos(pais):
    return render_template('bancos.html', pais=pais.capitalize())

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
