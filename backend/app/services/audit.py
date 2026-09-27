from app.db.models.users import AuditLog

def audit(db, user, action, resource, result="success"):
    db.add(AuditLog(actor_id=user.id if user else None,
                    role=user.role.value if user else "public",
                    action=action, resource=str(resource), result=result))
