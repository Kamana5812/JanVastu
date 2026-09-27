"""Recover a reproducible baseline for the user and need tables."""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.create_table("users",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("role", sa.Enum("citizen", "volunteer", "district_official", "state_planner", "national_planner", "auditor", "admin", name="userrole"), nullable=False),
        sa.Column("name", sa.String, nullable=False), sa.Column("mobile", sa.String, unique=True),
        sa.Column("email", sa.String, unique=True), sa.Column("password_hash", sa.String, nullable=False),
        sa.Column("preferred_language", sa.String, nullable=False, server_default="en"),
        sa.Column("state", sa.String), sa.Column("district", sa.String), sa.Column("locality", sa.String), sa.Column("ward_village", sa.String),
        sa.Column("status", sa.Enum("active", "pending_approval", "suspended", "rejected", name="userstatus"), nullable=False),
        sa.Column("token_version", sa.Integer, nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True)), sa.Column("last_active", sa.DateTime(timezone=True)))
    op.create_table("needs",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("category", sa.Enum("water", "road", "health", "school", "electricity", "sanitation", name="needcategory")),
        sa.Column("description", sa.String), sa.Column("affected_people", sa.Integer),
        sa.Column("location", Geometry("POINT", srid=4326)), sa.Column("address", sa.String),
        sa.Column("state", sa.String), sa.Column("district", sa.String),
        sa.Column("status", sa.Enum("reported", "verified", "planned", "resolved", "rejected", name="needstatus")),
        sa.Column("reported_by_id", sa.String, sa.ForeignKey("users.id")), sa.Column("created_at", sa.DateTime))
    op.create_table("evidence", sa.Column("id", sa.String, primary_key=True),
        sa.Column("need_id", sa.String, sa.ForeignKey("needs.id")), sa.Column("file_url", sa.String),
        sa.Column("uploaded_by_id", sa.String, sa.ForeignKey("users.id")), sa.Column("created_at", sa.DateTime))

def downgrade():
    raise RuntimeError("Destructive downgrade disabled. Restore a reviewed backup instead.")
