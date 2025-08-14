from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from app.models import db, Subscription, SubscriptionType, ClassSession, Attendance, ClientAvailability, Client

schedule_helper_bp = Blueprint('schedule_helper', __name__, url_prefix='/api/schedule-helper')


def get_week_bounds(current_date):
    start = current_date - timedelta(days=current_date.weekday())  # Monday
    end = start + timedelta(days=6)  # Sunday
    return start, end


@schedule_helper_bp.route('/<int:client_id>', methods=['GET'])
def get_schedule(client_id):
    current_date = datetime.utcnow()

    # Validate client exists
    client = db.session.get(Client, client_id)
    if not client:
        return jsonify({'error': 'Client not found'}), 404

    # Get active subscription
    subscription = Subscription.query.filter(
        Subscription.client_id == client_id,
        Subscription.status == 'active',
        Subscription.start_date <= current_date,
        (Subscription.end_date == None) | (Subscription.end_date >= current_date)
    ).first()

    if not subscription:
        return jsonify({'error': 'No active subscription found.'}), 400

    class_type_id = subscription.class_type_id
    sub_type = SubscriptionType.query.get(subscription.subscription_type_id)
    classes_per_week = sub_type.classes_per_week

    # Check how many sessions are already scheduled this week
    week_start, week_end = get_week_bounds(current_date)

    scheduled_sessions = (
        db.session.query(Attendance)
        .join(ClassSession)
        .filter(
            Attendance.client_id == client_id,
            ClassSession.class_type_id == class_type_id,
            ClassSession.scheduled_at >= week_start,
            ClassSession.scheduled_at <= week_end
        )
        .all()
    )

    remaining = classes_per_week - len(scheduled_sessions)
    if remaining <= 0:
        return jsonify({'message': 'Client has completed all scheduled classes this week.'})

    # Get client availability
    availability = ClientAvailability.query.filter_by(client_id=client_id).all()

    suggestions = []

    for slot in availability:
        day = slot.day_of_week  # 0 = Sunday, 6 = Saturday
        target_date = week_start + timedelta(days=day)
        start_dt = datetime.combine(target_date, slot.start_time)
        end_dt = datetime.combine(target_date, slot.end_time)

        # Find group sessions this client could join
        group_sessions = ClassSession.query.filter(
            ClassSession.class_type_id == class_type_id,
            ClassSession.scheduled_at >= start_dt,
            ClassSession.scheduled_at < end_dt,
            ClassSession.is_individual == False
        ).all()

        for session in group_sessions:
            attendee_count = Attendance.query.filter_by(session_id=session.id).count()
            if attendee_count < session.max_attendees:
                suggestions.append({
                    'action': 'join_existing_session',
                    'session_id': session.id,
                    'scheduled_at': session.scheduled_at.isoformat(),
                    'class_type_id': class_type_id
                })

    # If no group sessions found, suggest new time slots
    if not suggestions:
        for slot in availability:
            day = slot.day_of_week
            target_date = week_start + timedelta(days=day)
            proposed_time = datetime.combine(target_date, slot.start_time)

            existing = ClassSession.query.filter_by(scheduled_at=proposed_time).count()
            if existing == 0:
                suggestions.append({
                    'action': 'create_new_session',
                    'proposed_time': proposed_time.isoformat(),
                    'class_type_id': class_type_id,
                    'is_individual': True
                })
                break  # suggest only one

    return jsonify({
        'client_id': client_id,
        'remaining_sessions': remaining,
        'suggestions': suggestions
    })