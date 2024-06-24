from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_db', methods=['POST'])
def generate_db():
    data = request.get_json()
    db_name = data.get('db_name', '').strip()
    table_name = data.get('table_name', '').strip()
    fields = data.get('fields', [])

    if not db_name or not table_name or not fields:
        return jsonify({'message': 'Datos insuficientes para generar la base de datos.'}), 400

    if any(not field.get('name') or not field.get('type') for field in fields):
        return jsonify({'message': 'Todos los campos son obligatorios.'}), 400

    field_names = [field['name'] for field in fields]
    if len(field_names) != len(set(field_names)):
        return jsonify({'message': 'Los nombres de los campos deben ser únicos.'}), 400

    db_path = f"{db_name}.db"
    if os.path.exists(db_path):
        return jsonify({'message': f'La base de datos "{db_name}" ya existe.'}), 400

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    field_definitions = ", ".join([f"{field['name']} {field['type']}" for field in fields])
    create_table_query = f"CREATE TABLE {table_name} ({field_definitions});"
    cursor.execute(create_table_query)
    conn.commit()
    conn.close()

    return jsonify({'message': f'Base de datos "{db_name}" y tabla "{table_name}" creadas con éxito.'})

if __name__ == '__main__':
    app.run(debug=True)
