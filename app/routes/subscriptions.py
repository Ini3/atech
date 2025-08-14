from flask import Blueprint, request, jsonify
from app.models import db, Subscription, SubscriptionType, Client, ClassType
from datetime import datetime

subscriptions_bp = Blueprint('subscriptions', __name__, url_prefix='/api/subscriptions')

# -----------------------------
# SUBSCRIPTION TYPES
# -----------------------------

@subscriptions_bp.route('/types', methods=['GET'])
def get_subscription_types():
    types = SubscriptionType.query.all()
    return jsonify([{
        "id": t.id,
        "name": t.name,
        "classes_per_week": t.classes_per_week,
        "description": t.description
    } for t in types])

@subscriptions_bp.route('/types', methods=['POST'])
def create_subscription_type():
    data = request.get_json()
    sub_type = SubscriptionType(
        name=data['name'],
        classes_per_week=data['classes_per_week'],
        description=data.get('description')
    )
    db.session.add(sub_type)
    db.session.commit()
    return jsonify({"message": "Subscription type created", "id": sub_type.id}), 201

@subscriptions_bp.route('/types/<int:type_id>', methods=['PUT'])
def update_subscription_type(type_id):
    sub_type = SubscriptionType.query.get(type_id)
    if not sub_type:
        return jsonify({"error": "Subscription type not found"}), 404

    data = request.get_json()
    sub_type.name = data.get('name', sub_type.name)
    sub_type.classes_per_week = data.get('classes_per_week', sub_type.classes_per_week)
    sub_type.description = data.get('description', sub_type.description)
    db.session.commit()
    return jsonify({"message": "Subscription type updated"})

@subscriptions_bp.route('/types/<int:type_id>', methods=['DELETE'])
def delete_subscription_type(type_id):
    sub_type = SubscriptionType.query.get(type_id)
    if not sub_type:
        return jsonify({"error": "Subscription type not found"}), 404

    db.session.delete(sub_type)
    db.session.commit()
    return jsonify({"message": "Subscription type deleted"})

# -----------------------------
# SUBSCRIPTIONS
# -----------------------------

@subscriptions_bp.route('', methods=['GET'])
def get_subscriptions():
    subscriptions = Subscription.query.all()
    return jsonify([{
        "id": s.id,
        "client_id": s.client_id,
        "class_type_id": s.class_type_id,
        "subscription_type_id": s.subscription_type_id,
        "start_date": s.start_date.isoformat(),
        "end_date": s.end_date.isoformat() if s.end_date else None,
        "status": s.status
    } for s in subscriptions])

@subscriptions_bp.route('', methods=['POST'])
def create_subscription():
    data = request.get_json()

    # Validate required fields
    if not all(k in data for k in ('client_id', 'class_type_id', 'subscription_type_id', 'start_date')):
        return jsonify({"error": "Missing required fields"}), 400

    subscription = Subscription(
        client_id=data['client_id'],
        class_type_id=data['class_type_id'],
        subscription_type_id=data['subscription_type_id'],
        start_date=datetime.fromisoformat(data['start_date']),
        end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None,
        status=data.get('status', 'active')
    )
    db.session.add(subscription)
    db.session.commit()
    return jsonify({"message": "Subscription created", "id": subscription.id}), 201

@subscriptions_bp.route('/<int:subscription_id>', methods=['PUT'])
def update_subscription(subscription_id):
    subscription = Subscription.query.get(subscription_id)
    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404

    data = request.get_json()
    subscription.class_type_id = data.get('class_type_id', subscription.class_type_id)
    subscription.subscription_type_id = data.get('subscription_type_id', subscription.subscription_type_id)
    subscription.start_date = datetime.fromisoformat(data.get('start_date')) if data.get('start_date') else subscription.start_date
    subscription.end_date = datetime.fromisoformat(data.get('end_date')) if data.get('end_date') else subscription.end_date
    subscription.status = data.get('status', subscription.status)
    db.session.commit()
    return jsonify({"message": "Subscription updated"})

@subscriptions_bp.route('/<int:subscription_id>', methods=['DELETE'])
def delete_subscription(subscription_id):
    subscription = Subscription.query.get(subscription_id)
    if not subscription:
        return jsonify({"error": "Subscription not found"}), 404

    db.session.delete(subscription)
    db.session.commit()
    return jsonify({"message": "Subscription deleted"})
