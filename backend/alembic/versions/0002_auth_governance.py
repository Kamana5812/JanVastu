"""Persist applications, consent, sessions, rate limits, and immutable audit."""
from alembic import op
import sqlalchemy as sa
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

def upgrade():
    op.create_table("access_requests", sa.Column("id", sa.String, primary_key=True),
        sa.Column("user_id", sa.String, sa.ForeignKey("users.id"), unique=True, nullable=False),
        sa.Column("role_requested", sa.String, nullable=False), sa.Column("organization", sa.String),
        sa.Column("designation", sa.String), sa.Column("reason", sa.String), sa.Column("verification_info", sa.String),
        sa.Column("status", sa.String, nullable=False), sa.Column("reviewed_by", sa.String, sa.ForeignKey("users.id")),
        sa.Column("reviewed_at", sa.DateTime(timezone=True)), sa.Column("created_at", sa.DateTime(timezone=True)))
    op.create_table("consent_records", sa.Column("id", sa.String, primary_key=True),
        sa.Column("user_id", sa.String, sa.ForeignKey("users.id")), sa.Column("purpose", sa.String, nullable=False),
        sa.Column("language", sa.String), sa.Column("channel", sa.String), sa.Column("version", sa.String),
        sa.Column("status", sa.String), sa.Column("recorded_at", sa.DateTime(timezone=True)),
        sa.Column("withdrawn_at", sa.DateTime(timezone=True)))
    op.create_table("audit_logs", sa.Column("id", sa.String, primary_key=True),
        sa.Column("timestamp", sa.DateTime(timezone=True)), sa.Column("actor_id", sa.String),
        sa.Column("role", sa.String, nullable=False), sa.Column("action", sa.String, nullable=False),
        sa.Column("resource", sa.String, nullable=False), sa.Column("result", sa.String))
    op.execute("""CREATE FUNCTION janvastu_immutable_audit() RETURNS trigger AS $$
        BEGIN RAISE EXCEPTION 'Audit records are append-only'; END; $$ LANGUAGE plpgsql""")
    op.execute("CREATE TRIGGER audit_no_mutation BEFORE UPDATE OR DELETE ON audit_logs FOR EACH ROW EXECUTE FUNCTION janvastu_immutable_audit()")
    op.execute("CREATE TRIGGER audit_no_truncate BEFORE TRUNCATE ON audit_logs FOR EACH STATEMENT EXECUTE FUNCTION janvastu_immutable_audit()")
    op.execute("REVOKE UPDATE, DELETE, TRUNCATE ON audit_logs FROM PUBLIC")
    op.create_table("auth_challenges", sa.Column("id", sa.String, primary_key=True),
        sa.Column("user_id", sa.String, sa.ForeignKey("users.id")), sa.Column("purpose", sa.String, nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True)), sa.Column("attempts", sa.Integer))
    op.create_table("refresh_sessions", sa.Column("id", sa.String, primary_key=True),
        sa.Column("user_id", sa.String, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False), sa.Column("revoked_at", sa.DateTime(timezone=True)))
    op.create_table("rate_limits", sa.Column("key", sa.String, primary_key=True),
        sa.Column("count", sa.Integer, nullable=False), sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False))

def downgrade():
    raise RuntimeError("Destructive downgrade disabled.")
