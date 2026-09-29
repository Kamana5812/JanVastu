"""Provision an administrator without a public signup route or default password."""
import os
from app.db.base import SessionLocal
from app.db.models.users import User,UserRole,UserStatus,Consent
from app.core.security import get_password_hash
from app.services.audit import audit
def main():
    email=os.environ.get("ADMIN_EMAIL","").strip().lower()
    password=os.environ.get("ADMIN_PASSWORD","")
    if "@" not in email or len(password)<12 or len(password.encode())>72:
        raise SystemExit("Set ADMIN_EMAIL and ADMIN_PASSWORD (12 to 72 UTF-8 bytes).")
    with SessionLocal() as db:
        if db.query(User).filter_by(email=email).first():raise SystemExit("Account already exists; no changes made.")
        user=User(name=os.environ.get("ADMIN_NAME","JanVastu administrator"),email=email,
            password_hash=get_password_hash(password),role=UserRole.admin,status=UserStatus.active,preferred_language="en")
        db.add(user);db.flush()
        audit(db,user,"administrator.provisioned",user.id);db.commit()
    print("Administrator provisioned.")
if __name__=="__main__":main()
