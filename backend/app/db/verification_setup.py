"""Prepare only the explicitly named local verification database."""
import os,secrets
from pathlib import Path
from app.db.base import engine,SessionLocal
from app.db.provision import provision
from app.db.seed import seed_db
from app.db.models.users import User,UserRole,UserStatus,Consent
from app.core.security import get_password_hash
def main():
    if engine.url.database!="janvastu_verification":raise SystemExit("Requires janvastu_verification database.")
    password=secrets.token_urlsafe(30);os.environ["RUNTIME_DB_PASSWORD"]=password;provision();seed_db()
    with SessionLocal() as db:
        for role in UserRole:
            email="demo-"+role.value+"@example.org"
            u=db.query(User).filter_by(email=email).first()
            if not u:
                u=User(name="Synthetic "+role.value,email=email,password_hash=get_password_hash("Demo-only-password-27"),
                    role=role,status=UserStatus.active,state="Odisha",district="Puri",preferred_language="en")
                db.add(u);db.flush();db.add(Consent(user_id=u.id,purpose="account_and_reporting"))
        db.commit()
    url=engine.url.set(username="janvastu_api",password=password).render_as_string(hide_password=False)
    Path(".env.verification").write_text("DATABASE_URL="+url+"\nMINIO_ENDPOINT=localhost:9000\nMINIO_ACCESS_KEY=admin\nMINIO_SECRET_KEY=password\n",encoding="utf8")
    print("Isolated demo users and ignored runtime configuration prepared.")
if __name__=="__main__":main()
