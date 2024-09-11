from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar Flask-CORS
import mysql.connector

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Configurar la conexión a MySQL
db = mysql.connector.connect(
    host="ec2-34-207-71-37.compute-1.amazonaws.com",  # Dirección pública de tu base de datos
    user="myappuser",  # Usuario que creaste
    password="mypassword",  # Contraseña de tu usuario
    database="myappdb"  # Nombre de la base de datos
)

# Ruta para registrar un usuario
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombres = data['nombres']
    apellidos = data['apellidos']
    fecha_nacimiento = data['fecha_nacimiento']
    password = data['password']
    
    cursor = db.cursor()
    cursor.execute("INSERT INTO usuarios (nombres, apellidos, fecha_nacimiento, password) VALUES (%s, %s, %s, %s)", 
                   (nombres, apellidos, fecha_nacimiento, password))
    db.commit()
    return jsonify({"message": "Usuario registrado con éxito"}), 201

# Ruta para listar usuarios
@app.route('/users', methods=['GET'])
def list_users():
    cursor = db.cursor()
    cursor.execute("SELECT nombres, apellidos FROM usuarios")
    users = cursor.fetchall()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
