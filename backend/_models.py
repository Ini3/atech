from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize in your app factory or main app file:
db = SQLAlchemy()

class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    message = db.Column(db.Text, nullable=True)
    preferred_language = db.Column(db.String(20), nullable=False)  # 'euskera' or 'espanol'
    source_page = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to client if converted
    client = db.relationship('Client', backref='lead', uselist=False)

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    client_type = db.Column(db.String(20), default='trial')  # 'trial', 'subscribed', 'per_class'
    preferred_language = db.Column(db.String(20))
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))

    subscriptions = db.relationship('Subscription', backref='client', lazy=True)
    payments = db.relationship('PaymentRecord', backref='client', lazy=True)
    attendances = db.relationship('Attendance', backref='client', lazy=True)

class ClassType(db.Model):
    __tablename__ = 'class_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    language = db.Column(db.String(20))  # 'euskera', 'espanol'
    level = db.Column(db.String(10))     # 'A1', 'A2', 'B1'...
    description = db.Column(db.Text)
    price_per_class = db.Column(db.Float, nullable=True)
    is_subscription = db.Column(db.Boolean, default=False)  # indicates if this class supports subs
    stripe_price_id = db.Column(db.String(100))

    subscriptions = db.relationship('Subscription', backref='class_type', lazy=True)
    payments = db.relationship('PaymentRecord', backref='class_type', lazy=True)
    sessions = db.relationship('ClassSession', backref='class_type', lazy=True)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    class_type_id = db.Column(db.Integer, db.ForeignKey('class_types.id'), nullable=False)
    stripe_subscription_id = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')
    started_at = db.Column(db.DateTime, default=datetime.utcnow)

    payments = db.relationship('PaymentRecord', backref='subscription', lazy=True)

class PaymentRecord(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'), nullable=True)
    class_type_id = db.Column(db.Integer, db.ForeignKey('class_types.id'))
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.String(20))  # 'stripe', 'cash', 'transfer'
    payment_type = db.Column(db.String(20))    # 'subscription', 'per_class'
    payment_status = db.Column(db.String(20), default='pending')
    stripe_payment_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Session(db.Model):
    __tablename__ = 'class_sessions'
    id = db.Column(db.Integer, primary_key=True)
    class_type_id = db.Column(db.Integer, db.ForeignKey('class_types.id'))
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(100))
    zoom_link = db.Column(db.String(200))
    resources_url = db.Column(db.String(200))
    notes = db.Column(db.Text)

    attendances = db.relationship('Attendance', backref='class_session', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    class_session_id = db.Column(db.Integer, db.ForeignKey('class_sessions.id'))
    attended = db.Column(db.Boolean, default=True)
    paid = db.Column(db.Boolean, default=False)
    feedback = db.Column(db.Text)
