import os
import stripe
import datetime
from flask import Blueprint, request, jsonify, abort
from app.models import db, PaymentRecord, Subscription, Client, ClassType


stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

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


@payments.route('/create-checkout-session', methods=['POST'])
def create_checkout():

    stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

    data = request.get_json()
    client_id = data.get('client_id')
    class_type_id = data.get('class_type_id')

    # Optionally: Validate existence
    client = Client.query.get_or_404(client_id)
    class_type = ClassType.query.get_or_404(class_type_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_123abc456xyz',  # get from Stripe Dashboard
            'quantity': 1
        }],
        mode='subscription',
        success_url='https://yourdomain.com/success',
        cancel_url='https://yourdomain.com/cancel'
    
        client_reference_id=client.id,
        metadata={
            'class_type_id': class_type.id
        }
    )
    return jsonify({'id': session.id})


@payments.route('/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400
    except Exception as e:
        return f'Webhook error: {str(e)}', 400

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        client_id = session.get('client_reference_id')
        class_type_id = session.get('metadata', {}).get('class_type_id')
        stripe_sub_id = session.get('subscription')

        if client_id and class_type_id:
            # Create Subscription in DB
            existing = Subscription.query.filter_by(
                client_id=client_id,
                class_type_id=class_type_id
            ).first()

            if not existing:
                sub = Subscription(
                    client_id=client_id,
                    class_type_id=class_type_id,
                    stripe_subscription_id=stripe_sub_id,
                    status='active'
                )
                db.session.add(sub)
                db.session.commit()

    elif event['type'] == 'invoice.paid':
        invoice = event['data']['object']

        stripe_sub_id = invoice['subscription']
        amount = invoice['amount_paid'] / 100  # from cents to euros
        stripe_payment_id = invoice['payment_intent']

        # Find subscription by stripe ID
        subscription = Subscription.query.filter_by(
            stripe_subscription_id=stripe_sub_id
        ).first()

        if subscription:
            payment = PaymentRecord(
                subscription_id=subscription.id,
                amount=amount,
                payment_status='paid',
                stripe_payment_id=stripe_payment_id
            )
            db.session.add(payment)
            db.session.commit()

    elif event['type'] == 'invoice.payment_failed':
        # Optional: log or notify
        print('Payment failed for subscription.')

    return '', 200


@payments.route('/manual', methods=['POST'])
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


