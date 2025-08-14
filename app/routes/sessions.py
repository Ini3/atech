from flask import Blueprint, request, jsonify
from app.models import db, Session, Attendance
from datetime import datetime, timedelta

sessions_bp = Blueprint('sessions', __name__, url_prefix='/api/sessions')

# Get sessions in a date range (for calendar view)
@sessions_bp.route('', methods=['GET'])
def get_sessions():
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify({"error": "Missing start or end parameter"}), 400

    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)

    sessions = Session.query.filter(
        Session.scheduled_at >= start_dt,
        Session.scheduled_at <= end_dt
    ).all()

    results = []
    for s in sessions:
        results.append({
            "id": s.id,
            "title": f"Session: {s.class_type_id}",  # You can replace with class name
            "start": s.scheduled_at.isoformat(),
            "end": (s.scheduled_at + timedelta(minutes=s.duration_minutes)).isoformat(),
            "is_individual": s.is_individual
        })
    return jsonify(results)


@sessions_bp.route('', methods=['POST'])
def create_session():
    data = request.get_json()
    session = Session(
        class_type_id=data['class_type_id'],
        scheduled_at=datetime.fromisoformat(data['scheduled_at']),
        duration_minutes=data.get('duration_minutes', 60),
        is_individual=data.get('is_individual', True)
        #zoom_link=data.get('zoom_link'),
        #notes=data.get('notes')
    )
    db.session.add(session)
    db.session.commit()
    return jsonify({'message': 'Session created', 'id': session.id}), 201

@sessions_bp.route('/<int:class_type_id>', methods=['GET'])
def get_sessions(class_type_id):
    sessions = Session.query.filter_by(class_type_id=class_type_id).all()
    return jsonify([{
        'id': s.id,
        'date': s.date.isoformat(),
        'location': s.location,
        'zoom_link': s.zoom_link
    } for s in sessions])

@sessions_bp.route('/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    data = request.get_json()
    session.scheduled_at = datetime.fromisoformat(data['scheduled_at'])
    session.duration_minutes = data.get('duration_minutes', session.duration_minutes)
    db.session.commit()
    return jsonify({"message": "Session updated"})


@sessions_bp.route('/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    session = Session.query.get(session_id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    db.session.delete(session)
    db.session.commit()
    return jsonify({"message": "Session deleted"})