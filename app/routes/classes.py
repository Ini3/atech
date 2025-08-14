from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from app.models import db, ClassType, ClassSession, Attendance, Client

classes_bp = Blueprint('classes', __name__, url_prefix='/api/classes')

# -----------------------------
# CLASS TYPES
# -----------------------------

@classes_bp.route('/types', methods=['GET'])
def get_class_types():
    types = ClassType.query.all()
    return jsonify([{
        "id": t.id,
        "name": t.name,
        "level": t.level,
        "description": t.description,
        "created_at": t.created_at.isoformat()
    } for t in types])

@classes_bp.route('/types', methods=['POST'])
def create_class_type():
    data = request.get_json()
    class_type = ClassType(
        name=data['name'],
        level=data.get('level'),
        description=data.get('description')
    )
    db.session.add(class_type)
    db.session.commit()
    return jsonify({"message": "Class type created", "id": class_type.id}), 201

@classes_bp.route('/types/<int:type_id>', methods=['PUT'])
def update_class_type(type_id):
    class_type = ClassType.query.get(type_id)
    if not class_type:
        return jsonify({"error": "Class type not found"}), 404
    data = request.get_json()
    class_type.name = data.get('name', class_type.name)
    class_type.level = data.get('level', class_type.level)
    class_type.description = data.get('description', class_type.description)
    db.session.commit()
    return jsonify({"message": "Class type updated"})

@classes_bp.route('/types/<int:type_id>', methods=['DELETE'])
def delete_class_type(type_id):
    class_type = ClassType.query.get(type_id)
    if not class_type:
        return jsonify({"error": "Class type not found"}), 404
    db.session.delete(class_type)
    db.session.commit()
    return jsonify({"message": "Class type deleted"})

# -----------------------------
# ATTENDANCE (Client ↔ Session)
# -----------------------------

@classes_bp.route('/attendance', methods=['POST'])
def add_attendance():
    data = request.get_json()
    client_id = data['client_id']
    session_id = data['session_id']

    # Check if attendance already exists
    existing = Attendance.query.filter_by(client_id=client_id, session_id=session_id).first()
    if existing:
        return jsonify({"message": "Attendance already exists"}), 200

    attendance = Attendance(client_id=client_id, session_id=session_id)
    db.session.add(attendance)
    db.session.commit()
    return jsonify({"message": "Attendance recorded"}), 201

@classes_bp.route('/attendance', methods=['DELETE'])
def remove_attendance():
    data = request.get_json()
    client_id = data['client_id']
    session_id = data['session_id']

    attendance = Attendance.query.filter_by(client_id=client_id, session_id=session_id).first()
    if not attendance:
        return jsonify({"error": "Attendance not found"}), 404

    db.session.delete(attendance)
    db.session.commit()
    return jsonify({"message": "Attendance removed"})

@classes_bp.route('/attendance/<int:session_id>', methods=['GET'])
def get_attendance_for_session(session_id):
    records = Attendance.query.filter_by(session_id=session_id).all()
    return jsonify([{
        "client_id": r.client_id,
        "session_id": r.session_id,
        "attended": r.attended,
        "notes": r.notes
    } for r in records])

