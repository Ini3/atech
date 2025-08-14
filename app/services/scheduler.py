from datetime import datetime, timedelta
from app.models import db, PaymentRecord, Subscription, Client, ClassType
from models import Subscription, Session as ClassSession, Attendance, ClientAvailability


def get_week_bounds(current_date):
    start = current_date - timedelta(days=current_date.weekday())  # Monday
    end = start + timedelta(days=6)  # Sunday
    return start, end


def schedule_helper(db: db, client_id: int, current_date: datetime = None):
    current_date = current_date or datetime.utcnow()

    subscription = db.query(Subscription).filter(
        Subscription.client_id == client_id,
        Subscription.status == "active",
        Subscription.start_date <= current_date,
        (Subscription.end_date == None) | (Subscription.end_date >= current_date)
    ).first()

    if not subscription:
        return {"error": "No active subscription found."}

    class_type_id = subscription.class_type_id
    classes_per_week = subscription.subscription_type.classes_per_week

    week_start, week_end = get_week_bounds(current_date)

    scheduled_sessions = (
        db.query(Attendance)
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
        return {"message": "Client has completed all scheduled classes this week."}

    availability = db.query(ClientAvailability).filter_by(client_id=client_id).all()

    suggestions = []
    for slot in availability:
        day = slot.day_of_week
        target_date = week_start + timedelta(days=day)
        start_dt = datetime.combine(target_date, slot.start_time)
        end_dt = datetime.combine(target_date, slot.end_time)

        matching_sessions = (
            db.query(ClassSession)
            .filter(
                ClassSession.class_type_id == class_type_id,
                ClassSession.scheduled_at >= start_dt,
                ClassSession.scheduled_at < end_dt,
                ClassSession.is_individual == False
            )
            .all()
        )

        for session in matching_sessions:
            attendee_count = db.query(Attendance).filter_by(session_id=session.id).count()
            if attendee_count < session.max_attendees:
                suggestions.append({
                    "action": "join_existing_session",
                    "session_id": session.id,
                    "scheduled_at": session.scheduled_at.isoformat(),
                    "class_type_id": class_type_id
                })

    if not suggestions:
        for slot in availability:
            day = slot.day_of_week
            target_date = week_start + timedelta(days=day)
            start_dt = datetime.combine(target_date, slot.start_time)

            existing_teacher_sessions = db.query(ClassSession).filter(
                ClassSession.scheduled_at == start_dt
            ).count()

            if existing_teacher_sessions == 0:
                suggestions.append({
                    "action": "create_new_session",
                    "proposed_time": start_dt.isoformat(),
                    "class_type_id": class_type_id,
                    "is_individual": True
                })
                break

    return {
        "client_id": client_id,
        "remaining_sessions": remaining,
        "suggestions": suggestions
    }
