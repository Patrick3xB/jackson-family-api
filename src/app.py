from flask import Flask, request, jsonify
from flask_cors import CORS
from datastructure import FamilyStructure
from utils import APIException, generate_sitemap

# Inicializa la familia
jackson_family = FamilyStructure("Jackson")

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Manejo de errores
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Sitemap con endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# Obtener todos los miembros
@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# Obtener un miembro por ID
@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200

# Añadir un nuevo miembro
@app.route('/members', methods=['POST'])
def add_member():
    body = request.get_json()
    if body is None:
        return jsonify({"error": "Missing request body"}), 400

    jackson_family.add_member(body)
    return jsonify({"msg": "Member added successfully"}), 200

# Eliminar un miembro por ID
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    success = jackson_family.delete_member(member_id)
    if not success:
        return jsonify({"error": "Member not found"}), 404
    return jsonify({"done": True}), 200

# Main
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
