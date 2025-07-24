from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/remesas')
def remesas():
    return render_template('remesas.html')

@app.route('/bancos/venezuela')
def bancos_venezuela():
    return render_template('bancos_venezuela.html')

@app.route('/bancos/peru')
def bancos_peru():
    return render_template('bancos_peru.html')

@app.route('/bancos/chile')
def bancos_chile():
    return render_template('bancos_chile.html')

@app.route('/bancos/colombia')
def bancos_colombia():
    return render_template('bancos_colombia.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
