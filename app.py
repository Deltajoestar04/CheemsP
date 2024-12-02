from flask import Flask, request, jsonify, render_template, abort
from entities.ciudad import Ciudad

app = Flask(__name__)

# Página de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para mostrar todas las ciudades en una vista HTML
@app.route('/ciudades')
def ciudades():
    try:
        ciudades = Ciudad.get_all()
        return render_template('ciudades.html', ciudades=ciudades)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

# Página para registrar una nueva ciudad
@app.route('/ciudad-registro', methods=['GET'])
def ciudad_registro():
    return render_template('ciudad.html')

# Ruta para obtener todas las ciudades en formato JSON
@app.route('/ciudad', methods=['GET'])
def get_ciudades():
    try:
        ciudades = Ciudad.get_all()
        return jsonify(ciudades), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para guardar una nueva ciudad
@app.route('/ciudad', methods=['POST'])
def save():
    try:
        data = request.get_json()
        if not data or 'nombre' not in data or 'codigo' not in data:
            return jsonify({'error': 'Datos inválidos. Se requiere "nombre" y "codigo".'}), 400

        ciudad = Ciudad(nombre=data['nombre'], codigo=data['codigo'])
        ciudad_id = Ciudad.save(ciudad)
        return jsonify({'id': ciudad_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para actualizar una ciudad existente
@app.route('/ciudad/<int:id>', methods=['PUT'])
def update(id):
    try:
        data = request.get_json()
        if not data or 'nombre' not in data or 'codigo' not in data:
            return jsonify({'error': 'Datos inválidos. Se requiere "nombre" y "codigo".'}), 400

        ciudad = Ciudad(nombre=data['nombre'], codigo=data['codigo'])
        result = Ciudad.update(id, ciudad)

        if result == 0:
            return jsonify({'error': 'El registro de ciudad no existe'}), 404
        return jsonify({'id': id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Manejo de errores para rutas no encontradas
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Manejo de errores genéricos
@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
