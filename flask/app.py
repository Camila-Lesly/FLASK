from flask import Flask, request, jsonify, render_template, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = '1234'  # Necesario para flash
app.secret_key = '1234' #Necesario para iniciar Flask


# Datos de ejemplo para usuarios
usuarios = [
    {'nombre': 'Ana López', 'email': 'ana@ejemplo.com'},
    {'nombre': 'Carlos García', 'email': 'carlos@ejemplo.com'},
    {'nombre': 'María Pérez', 'email': 'maria@ejemplo.com'}
]


# Lógica para crear un nuevo contacto
def crear_contacto(nombre, email, mensaje):
    contacto = {'nombre': nombre, 'email': email, 'mensaje': mensaje}
    usuarios.append(contacto)
    return contacto

# Página de inicio: formulario de contacto
@app.route('/', methods=['GET', 'POST'])
def home():
    mensaje_gracias = None
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')
        if nombre and email:
            crear_contacto(nombre, email, mensaje)
            mensaje_gracias = f'¡Gracias {nombre}! Te contactaremos en {email}'
            return render_template('index.html', mensaje_gracias=mensaje_gracias)
        else:
            flash('Por favor completa todos los campos')
            return redirect(url_for('home'))
    return render_template('index.html')

# Ruta con parámetro
@app.route('/usuario/<nombre>')
def saludar(nombre):
    return f"<h2>Hola {nombre.title()}!</h2>"


# Ruta API JSON paginada
@app.route('/api/usuarios')
def api_usuarios():
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    usuarios = [
        {"id": i, "nombre": f"Usuario {i}"}
        for i in range((page-1)*limit + 1, page*limit + 1)
    ]
    return jsonify({"page": page, "limit": limit, "usuarios": usuarios})


# Ruta con múltiples métodos HTTP
@app.route('/mensaje', methods=['GET', 'POST'])
def mensaje():
    if request.method == 'POST':
        data = request.get_json() or {}
        mensaje = data.get('mensaje', 'No se envió mensaje')
        return jsonify({"respuesta": f"Mensaje recibido: {mensaje}"})
    else:
        return '''
            <form method="post" action="/mensaje">
                <input type="text" name="mensaje" placeholder="Escribe un mensaje">
                <input type="submit" value="Enviar">
            </form>
        '''



# Página 2: muestra tabla de usuarios
@app.route('/usuarios')
def usuarios_lista():
    return render_template('usuarios.html', usuarios=usuarios)

# API JSON para formulario de contacto usando query params
@app.route('/api/contacto')
def api_contacto():
    nombre = request.args.get('nombre', '')
    email = request.args.get('email', '')
    mensaje = request.args.get('mensaje', '')
    if not (nombre and email and mensaje):
        return jsonify({"error": "Faltan datos en la consulta"}), 400
    return jsonify({
        "nombre": nombre,
        "email": email,
        "mensaje": mensaje,
        "status": "Mensaje recibido correctamente"
    })


# Redirección de vieja ruta
@app.route('/vieja-ruta')
def vieja_ruta():
    return 'Esta es la vieja ruta', 301, {'Location': '/nueva-ruta'}

# Manejador de error 404 personalizado
@app.errorhandler(404)
def pagina_no_encontrada(e):
    return jsonify({"error": "Página no encontrada"}), 404

if __name__ == '__main__':
    app.run(debug=True)
