from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize in your app factory or main app file:
db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    #client_type = db.Column(db.String(20), default='trial')  # 'trial', 'subscribed', 'per_class'
    #preferred_language = db.Column(db.String(20))
    #lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))

    subscriptions = db.relationship('Subscription', backref='client', lazy=True)
    attendances = db.relationship('Attendance', backref='client', lazy=True)
    #payments = db.relationship('PaymentRecord', backref='client', lazy=True)

class ClientRequest(db.Model):
    __tablename__ = "client_requests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    preferred_class_type_id = db.Column(db.Integer, db.ForeignKey("class_types.id"), nullable=True)
    message = db.Column(db.Text)
    status = db.Column(db.String, default="pending")  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    preferred_class_type = db.relationship("ClassType", back_populates="client_requests")

class ClientAvailability(db.Model):
    __tablename__ = "client_availabilities"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    day_of_week = db.Column(db.Integer, nullable=False)  # 0 = Sunday
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    client = db.relationship("Client")
    
class ClassType(db.Model):
    __tablename__ = 'class_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    language = db.Column(db.String(20))  # 'euskera', 'espanol'
    level = db.Column(db.String(10))     # 'A1', 'A2', 'B1'...
    description = db.Column(db.Text)
    price_per_class = db.Column(db.Float, nullable=True)
    is_subscription = db.Column(db.Boolean, default=False)  # indicates if this class supports subs
    #stripe_price_id = db.Column(db.String(100))

    client_requests = db.relationship("ClientRequest", back_populates="preferred_class_type")
    subscriptions = db.relationship('Subscription', backref='class_type', lazy=True)
    sessions = db.relationship('ClassSession', backref='class_type', lazy=True)
    #payments = db.relationship('PaymentRecord', backref='class_type', lazy=True)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    class_type_id = db.Column(db.Integer, db.ForeignKey('class_types.id'), nullable=False)
    subscription_type_id = db.Column(db.Integer, db.ForeignKey("subscription_types.id"))
    #stripe_subscription_id = db.Column(db.String(100))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String, default="active")  # active, paused, cancelled

    client = db.relationship("Client", back_populates="subscriptions")
    class_type = db.relationship("ClassType", back_populates="subscriptions")
    subscription_type = db.relationship("SubscriptionType", back_populates="subscriptions")
    #payments = db.relationship('PaymentRecord', backref='subscription', lazy=True)

class SubscriptionType(db.Model):
    __tablename__ = "subscription_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    classes_per_week = db.Column(db.Integer, nullable=False)  # 0 for pay-per-class
    description = db.Column(db.Text)

    subscriptions = db.relationship("Subscription", back_populates="subscription_type")


class Session(db.Model):
    __tablename__ = 'class_sessions'
    id = db.Column(db.Integer, primary_key=True)
    class_type_id = db.Column(db.Integer, db.ForeignKey('class_types.id'))
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    is_individual = db.Column(db.Boolean, default=True)
    max_attendees = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    zoom_link = db.Column(db.String(200))
    #resources_url = db.Column(db.String(200))
    #notes = db.Column(db.Text)

    class_type = db.relationship("ClassType", back_populates="sessions")
    attendances = db.relationship('Attendance', backref='class_session', lazy=True)

class Attendance(db.Model):
    __tablename__ = 'attendance'
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"), primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), primary_key=True)
    attended = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    #feedback = db.Column(db.Text)

    client = db.relationship("Client", back_populates="attendances")
    session = db.relationship("Session", back_populates="attendances")






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