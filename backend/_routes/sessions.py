from flask import Blueprint, request, jsonify
from app.models import db, ClassSession
from datetime import datetime

sessions_bp = Blueprint('sessions', __name__, url_prefix='/api/sessions')

@sessions_bp.route('', methods=['POST'])
def create_session():
    data = request.get_json()
    session = ClassSession(
        class_type_id=data['class_type_id'],
        date=datetime.strptime(data['date'], '%Y-%m-%d %H:%M'),
        location=data.get('location'),
        zoom_link=data.get('zoom_link'),
        resources_url=data.get('resources_url'),
        notes=data.get('notes')
    )
    db.session.add(session)
    db.session.commit()
    return jsonify({'message': 'Session created', 'id': session.id}), 201

@sessions_bp.route('/<int:class_type_id>', methods=['GET'])
def get_sessions(class_type_id):
    sessions = ClassSession.query.filter_by(class_type_id=class_type_id).all()
    return jsonify([{
        'id': s.id,
        'date': s.date.isoformat(),
        'location': s.location,
        'zoom_link': s.zoom_link
    } for s in sessions])


# Manual Payment Record (non-Stripe)
@sessions_bp.route('/payments/manual', methods=['POST'])
def manual_payment():
    data = request.get_json()
    payment = PaymentRecord(
        client_id=data['client_id'],
        class_type_id=data['class_type_id'],
        amount=data['amount'],
        payment_method=data['payment_method'],
        payment_type='per_class',
        payment_status='paid',
        created_at=datetime.utcnow()
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({'message': 'Payment recorded'}), 201