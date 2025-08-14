from flask import Blueprint, request, jsonify, abort
from app.models import db, Lead, Client, ClassType
import os

api = Blueprint('api', __name__, url_prefix='/api')

API_KEY = os.environ.get("ADMIN_API_KEY")

def require_api_key():
    if request.headers.get('X-API-KEY') != API_KEY:
        abort(401, description="Unauthorized - Invalid API Key")

# --- Swagger Metadata ---
@api.route('/', methods=['GET'])
def api_info():
    return jsonify({
        "name": "KA teaching API",
        "version": "1.0",
        "endpoints": [
            "/api/leads",
            "/api/clients",
            "/api/classes",
            "/api/payments"
        ]
    })

# --- Leads ---
@api.route('/leads', methods=['GET'])
def get_leads():
    leads = Lead.query.all()
    return jsonify([{
        'id': lead.id,
        'name': lead.name,
        'email': lead.email,
        'phone': lead.phone,
        'message': lead.message,
        'preferred_language': lead.preferred_language,
        'created_at': lead.created_at.isoformat()
    } for lead in leads])

@api.route('/leads', methods=['POST'])
def create_lead():
    data = request.json
    lead = Lead(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        message=data.get('message'),
        preferred_language=data.get('preferred_language'),
        source_page=data.get('source_page')
    )
    db.session.add(lead)
    db.session.commit()
    return jsonify({'id': lead.id}), 201

@api.route('/leads/<int:lead_id>', methods=['GET'])
def get_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    return jsonify({
        'id': lead.id,
        'name': lead.name,
        'email': lead.email,
        'phone': lead.phone,
        'message': lead.message,
        'preferred_language': lead.preferred_language,
        'created_at': lead.created_at.isoformat()
    })

@api.route('/leads/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    data = request.json
    lead.name = data.get('name', lead.name)
    lead.email = data.get('email', lead.email)
    lead.phone = data.get('phone', lead.phone)
    lead.message = data.get('message', lead.message)
    lead.preferred_language = data.get('preferred_language', lead.preferred_language)
    db.session.commit()
    return jsonify({'message': 'Lead updated'})

@api.route('/leads/<int:lead_id>', methods=['DELETE'])
def delete_lead(lead_id):
    lead = Lead.query.get_or_404(lead_id)
    db.session.delete(lead)
    db.session.commit()
    return jsonify({'message': 'Lead deleted'})


# --- Clients ---
@api.route('/clients', methods=['GET'])
def get_clients():
    clients = Client.query.all()
    return jsonify([client_to_dict(c) for c in clients])

@api.route('/clients/<int:client_id>', methods=['GET'])
def get_client(client_id):
    client = Client.query.get_or_404(client_id)
    return jsonify(client_to_dict(client))

@api.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    client = Client(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        lead_id=data.get('lead_id')
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({'id': client.id}), 201

@api.route('/clients/<int:client_id>', methods=['PUT'])
def update_client(client_id):
    client = Client.query.get_or_404(client_id)
    data = request.json
    client.name = data.get('name', client.name)
    client.email = data.get('email', client.email)
    client.phone = data.get('phone', client.phone)
    db.session.commit()
    return jsonify({'message': 'Client updated'})

@api.route('/clients/<int:client_id>', methods=['DELETE'])
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({'message': 'Client deleted'})

# --- Class Types ---
@api.route('/classes', methods=['GET'])
def get_classes():
    classes = ClassType.query.all()
    return jsonify([class_to_dict(c) for c in classes])

@api.route('/classes/<int:class_id>', methods=['GET'])
def get_class(class_id):
    cls = ClassType.query.get_or_404(class_id)
    return jsonify(class_to_dict(cls))

@api.route('/classes', methods=['POST'])
def create_class():
    data = request.json
    class_type = ClassType(
        language=data.get('language'),
        mode=data.get('mode'),
        price=data.get('price'),
        description=data.get('description')
    )
    db.session.add(class_type)
    db.session.commit()
    return jsonify({'id': class_type.id}), 201

@api.route('/classes/<int:class_id>', methods=['PUT'])
def update_class(class_id):
    cls = ClassType.query.get_or_404(class_id)
    data = request.json
    cls.language = data.get('language', cls.language)
    cls.mode = data.get('mode', cls.mode)
    cls.price = data.get('price', cls.price)
    cls.description = data.get('description', cls.description)
    db.session.commit()
    return jsonify({'message': 'ClassType updated'})

@api.route('/classes/<int:class_id>', methods=['DELETE'])
def delete_class(class_id):
    cls = ClassType.query.get_or_404(class_id)
    db.session.delete(cls)
    db.session.commit()
    return jsonify({'message': 'ClassType deleted'})



# --- Helper Serializers ---
def lead_to_dict(lead):
    return {
        'id': lead.id,
        'name': lead.name,
        'email': lead.email,
        'phone': lead.phone,
        'message': lead.message,
        'preferred_language': lead.preferred_language,
        'source_page': lead.source_page,
        'created_at': lead.created_at.isoformat()
    }

def client_to_dict(client):
    return {
        'id': client.id,
        'name': client.name,
        'email': client.email,
        'phone': client.phone,
        'lead_id': client.lead_id,
        'created_at': client.created_at.isoformat()
    }

def class_to_dict(cls):
    return {
        'id': cls.id,
        'language': cls.language,
        'mode': cls.mode,
        'price': cls.price,
        'description': cls.description
    }
