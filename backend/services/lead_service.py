from app.models import db, ClientLead

def create_lead(data):
    lead = ClientLead(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        message=data.get('message'),
        language_interest=data.get('language'),
        source_page=data.get('source')
    )
    db.session.add(lead)
    db.session.commit()
    return lead
