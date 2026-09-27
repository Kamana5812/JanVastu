"""Consent-aware reporting, media metadata, history, and real pipeline telemetry."""
from alembic import op
import sqlalchemy as sa
revision="0003"
down_revision="0002"
branch_labels=None
depends_on=None

def upgrade():
    with op.get_context().autocommit_block():
        for value in ("transport","housing","other"):
            op.execute(f"ALTER TYPE needcategory ADD VALUE IF NOT EXISTS '{value}'")
    for column in [
        sa.Column("locality",sa.String),sa.Column("ward_village",sa.String),
        sa.Column("consent_id",sa.String,sa.ForeignKey("consent_records.id")),
        sa.Column("project_id",sa.String),sa.Column("client_id",sa.String),sa.Column("payload_hash",sa.String),
        sa.Column("language",sa.String),sa.Column("geocoding_source",sa.String),
        sa.Column("moderation_reason",sa.String),sa.Column("updated_at",sa.DateTime(timezone=True)),
        sa.Column("verified_by_id",sa.String,sa.ForeignKey("users.id")),sa.Column("verified_at",sa.DateTime(timezone=True))]:
        op.add_column("needs",column)
    op.alter_column("needs","created_at",type_=sa.DateTime(timezone=True),postgresql_using="created_at AT TIME ZONE 'UTC'")
    op.create_unique_constraint("uq_need_client","needs",["reported_by_id","client_id"])
    for column in [sa.Column("content_type",sa.String),sa.Column("size_bytes",sa.Integer),
                   sa.Column("anonymized",sa.Boolean,nullable=False,server_default=sa.false())]:
        op.add_column("evidence",column)
    op.alter_column("evidence","created_at",type_=sa.DateTime(timezone=True),postgresql_using="created_at AT TIME ZONE 'UTC'")
    op.create_table("need_events",sa.Column("id",sa.String,primary_key=True),
        sa.Column("need_id",sa.String,sa.ForeignKey("needs.id"),nullable=False),sa.Column("status",sa.String,nullable=False),
        sa.Column("created_at",sa.DateTime(timezone=True)))
    op.create_table("pipeline_runs",sa.Column("id",sa.String,primary_key=True),
        sa.Column("need_id",sa.String,sa.ForeignKey("needs.id")),sa.Column("stage",sa.String,nullable=False),
        sa.Column("model_version",sa.String,nullable=False),sa.Column("latency_ms",sa.Float,nullable=False),
        sa.Column("success",sa.Boolean,nullable=False),sa.Column("language",sa.String),
        sa.Column("category",sa.String),sa.Column("confidence",sa.Float),sa.Column("created_at",sa.DateTime(timezone=True)))

def downgrade():
    raise RuntimeError("Destructive downgrade disabled.")
