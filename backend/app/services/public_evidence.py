from sqlalchemy import exists
from sqlalchemy.orm import aliased
from app.db.models.needs import Evidence,Need
from app.db.models.users import Consent
def eligible(db):
    account=aliased(Consent)
    active_account=exists().where(account.user_id==Need.reported_by_id,account.purpose=="account_and_reporting",account.status=="active")
    return db.query(Evidence).join(Need,Need.id==Evidence.need_id).join(Consent,Consent.id==Need.consent_id).filter(
        Evidence.anonymized.is_(True),Evidence.public_file_url.isnot(None),Consent.status=="active",active_account)
