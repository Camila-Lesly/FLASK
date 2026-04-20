from flask import Blueprint, render_template, request, flash, redirect, url_for

# Datos de ejemplo para usuarios (importar desde app principal si es necesario)
usuarios = [
    {'nombre': 'Ana López', 'email': 'ana@ejemplo.com'},
    {'nombre': 'Carlos García', 'email': 'carlos@ejemplo.com'},
    {'nombre': 'María Pérez', 'email': 'maria@ejemplo.com'}
]

def crear_contacto(nombre, email, mensaje):
    contacto = {'nombre': nombre, 'email': email, 'mensaje': mensaje}
    usuarios.append(contacto)
    return contacto

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def home():
    mensaje_gracias = None
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')
        if nombre and email:
            crear_contacto(nombre, email, mensaje)
            mensaje_gracias = f'¡Gracias {nombre}! Te contactaremos en {email}'
            return render_template('index.html', mensaje_gracias=mensaje_gracias, usuarios=usuarios)
        else:
            flash('Por favor completa todos los campos')
            return redirect(url_for('main.home'))
    return render_template('index.html', usuarios=usuarios)

@main_bp.route('/usuarios')
def usuarios_lista():
    return render_template('usuarios.html', usuarios=usuarios)
