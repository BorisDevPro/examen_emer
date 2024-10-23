from flask import Flask, request, render_template,redirect,url_for,session

app = Flask(__name__)
app.secret_key = 'unaclavesecreta'

@app.route("/")
def index():
    if 'producto' not in session:
        session['producto'] = []

    producto = session.get('producto',[])
    return render_template('index.html',producto = producto)

def generar_id():
    if 'producto' in session and len(session['producto']) > 0:
        return max(item['id'] for item in session['producto']) + 1
    else:
        return 1

@app.route("/nuevo",methods=['GET','POST'])
def nuevo():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        fecha = request.form['fecha']
        categoria = request.form['categoria']

        nuevo_producto = {
            'id' : generar_id(),
            'descripcion': descripcion,
            'cantidad': cantidad,
            'precio': precio,
            'fecha':fecha,
            'categoria': categoria

        }

        if 'producto' not in session:
            session['producto'] = []
        
        session['producto'].append(nuevo_producto)
        session.modified = True
        return redirect(url_for('index'))
    return render_template('nuevo.html')

@app.route('/editar/<int:id>',methods=['GET','POST'])
def editar(id):
    lista_producto = session.get('producto',[])
    productos = next((c for c in lista_producto if c['id'] == id), None)
    if not productos:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        productos['descripcion'] = request.form['descripcion']
        productos['cantidad'] = request.form['cantidad']
        productos['precio'] = request.form['precio']
        productos['fecha'] = request.form['fecha']
        productos['categoria'] = request.form['categoria']
        session.modified = True
        return redirect(url_for('index'))
    return render_template('editar.html',productos = productos)
    
@app.route("/eliminar/<int:id>",methods=["POST"])
def eliminar(id):
    lista_producto = session.get('producto',[])
    productos = next((c for c in lista_producto if c['id'] == id), None)
    if productos:
        session['producto'].remove(productos)
        session.modified = True
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

