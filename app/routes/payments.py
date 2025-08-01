import os
from flask import Blueprint, request, jsonify, abort
from app.models import db, PaymentRecord

payments = Blueprint('payments', __name__, url_prefix='/api/payments')

API_KEY = os.environ.get("ADMIN_API_KEY")

def require_api_key():
    if request.headers.get('X-API-KEY') != API_KEY:
        abort(401, description="Unauthorized - Invalid API Key")

# GET all payments
@payments.route('/', methods=['GET'])
def get_payments():
    require_api_key()
    payments = PaymentRecord.query.all()
    return jsonify([payment_to_dict(p) for p in payments])

# GET payment by ID
@payments.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    require_api_key()
    payment = PaymentRecord.query.get_or_404(payment_id)
    return jsonify(payment_to_dict(payment))

# POST create new payment
@payments.route('/', methods=['POST'])
def create_payment():
    require_api_key()
    data = request.json
    payment = PaymentRecord(
        client_id=data.get('client_id'),
        class_type_id=data.get('class_type_id'),
        amount=data.get('amount'),
        currency=data.get('currency', 'EUR'),
        payment_status=data.get('payment_status', 'pending'),
        stripe_payment_id=data.get('stripe_payment_id')
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({'id': payment.id}), 201

# PUT update payment
@payments.route('/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    require_api_key()
    payment = PaymentRecord.query.get_or_404(payment_id)
    data = request.json
    payment.amount = data.get('amount', payment.amount)
    payment.currency = data.get('currency', payment.currency)
    payment.payment_status = data.get('payment_status', payment.payment_status)
    payment.stripe_payment_id = data.get('stripe_payment_id', payment.stripe_payment_id)
    db.session.commit()
    return jsonify({'message': 'Payment updated'})

# DELETE payment
@payments.route('/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    require_api_key()
    payment = PaymentRecord.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted'})

# Helper

def payment_to_dict(payment):
    return {
        'id': payment.id,
        'client_id': payment.client_id,
        'class_type_id': payment.class_type_id,
        'amount': payment.amount,
        'currency': payment.currency,
        'payment_status': payment.payment_status,
        'stripe_payment_id': payment.stripe_payment_id,
        'created_at': payment.created_at.isoformat()
    }


