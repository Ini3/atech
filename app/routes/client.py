from flask import Blueprint, request, jsonify
from app.models import db, Client, ClientRequest, ClientAvailability
from datetime import datetime

client_bp = Blueprint('client', __name__, url_prefix='/api/clients')

# -----------------------------
# CLIENT CRUD
# -----------------------------

@client_bp.route('', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "email": c.email,
        "created_at": c.created_at.isoformat()
    } for c in clients])

@client_bp.route('/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    return jsonify({
        "id": client.id,
        "name": client.name,
        "email": client.email,
        "created_at": client.created_at.isoformat()
    })

    
@client_bp.route('', methods=['POST'])
def create_client():
    data = request.get_json()
    client = Client(
        name=data['name'],
        email=data['email']
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({"message": "Client created", "id": client.id}), 201

@client_bp.route('/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    data = request.get_json()
    client.name = data.get('name', client.name)
    client.email = data.get('email', client.email)
    db.session.commit()
    return jsonify({"message": "Client updated"})

@client_bp.route('/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get(client_id)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "Client deleted"})

# -----------------------------
# CLIENT REQUESTS
# -----------------------------

@client_bp.route('/requests', methods=['POST'])
def create_client_request():
    data = request.get_json()
    request_obj = ClientRequest(
        name=data['name'],
        email=data['email'],
        preferred_class_type_id=data.get('preferred_class_type_id'),
        message=data.get('message'),
        status='pending'
    )
    db.session.add(request_obj)
    db.session.commit()
    return jsonify({"message": "Client request submitted", "id": request_obj.id}), 201

@client_bp.route('/requests', methods=['GET'])
def get_client_requests():
    requests = ClientRequest.query.all()
    return jsonify([{
        "id": r.id,
        "name": r.name,
        "email": r.email,
        "preferred_class_type_id": r.preferred_class_type_id,
        "status": r.status,
        "created_at": r.created_at.isoformat()
    } for r in requests])

@client_bp.route('/requests/<int:request_id>', methods=['PUT'])
def update_client_request_status(request_id):
    request_obj = ClientRequest.query.get(request_id)
    if not request_obj:
        return jsonify({"error": "Request not found"}), 404
    data = request.get_json()
    request_obj.status = data.get('status', request_obj.status)
    db.session.commit()
    return jsonify({"message": "Request status updated"})

@client_bp.route('/requests/<int:request_id>', methods=['DELETE'])
def delete_client_request(request_id):
    request_obj = ClientRequest.query.get(request_id)
    if not request_obj:
        return jsonify({"error": "Request not found"}), 404
    db.session.delete(request_obj)
    db.session.commit()
    return jsonify({"message": "Request deleted"})

# -----------------------------
# CLIENT AVAILABILITY
# -----------------------------

@client_bp.route('/<int:client_id>/availability', methods=['GET'])
def get_client_availability(client_id):
    availability = ClientAvailability.query.filter_by(client_id=client_id).all()
    return jsonify([{
        "id": a.id,
        "day_of_week": a.day_of_week,
        "start_time": a.start_time.strftime('%H:%M'),
        "end_time": a.end_time.strftime('%H:%M')
    } for a in availability])

@client_bp.route('/<int:client_id>/availability', methods=['POST'])
def add_client_availability(client_id):
    data = request.get_json()
    availability = ClientAvailability(
        client_id=client_id,
        day_of_week=data['day_of_week'],
        start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
        end_time=datetime.strptime(data['end_time'], '%H:%M').time()
    )
    db.session.add(availability)
    db.session.commit()
    return jsonify({"message": "Availability added", "id": availability.id}), 201

@client_bp.route('/<int:client_id>/availability/<int:availability_id>', methods=['DELETE'])
def delete_client_availability(client_id, availability_id):
    availability = ClientAvailability.query.get(availability_id)
    if not availability or availability.client_id != client_id:
        return jsonify({"error": "Availability not found"}), 404
    db.session.delete(availability)
    db.session.commit()
    return jsonify({"message": "Availability deleted"})