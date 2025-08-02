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
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))

class ClassType(db.Model):
    __tablename__ = 'class_types'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(20), nullable=False)  # 'euskera' or 'espanol'
    mode = db.Column(db.String(20), nullable=False)      # 'virtual' or 'presencial'
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)

class PaymentRecord(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    class_type_id = db.Column(db.Integer, db.ForeignKey('class_types.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='EUR')
    payment_status = db.Column(db.String(20), default='pending')  # 'paid', 'failed'
    stripe_payment_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    client = db.relationship('Client', backref=db.backref('payments', lazy=True))
    class_type = db.relationship('ClassType', backref=db.backref('payments', lazy=True))
