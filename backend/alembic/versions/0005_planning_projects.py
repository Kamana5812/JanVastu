"""Planning context, source-labelled public projects, and integration status."""
from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry
revision="0005"
down_revision="0004"
branch_labels=None
depends_on=None
def upgrade():
    op.create_table("planning_context",sa.Column("id",sa.String,primary_key=True),
        sa.Column("state",sa.String,nullable=False),sa.Column("district",sa.String,nullable=False),
        sa.Column("locality",sa.String,nullable=False),sa.Column("ward_village",sa.String,nullable=False),
        sa.Column("category",sa.String,nullable=False),sa.Column("latitude",sa.Float,nullable=False),
        sa.Column("longitude",sa.Float,nullable=False),sa.Column("infrastructure_stock",sa.Float,nullable=False),
        sa.Column("planned_investment",sa.Float,nullable=False),sa.Column("vulnerability",sa.Float,nullable=False),
        sa.Column("source",sa.String,nullable=False),sa.Column("is_sample",sa.Boolean,nullable=False),
        sa.UniqueConstraint("state","district","locality","ward_village","category",name="uq_planning_area"))
    op.create_table("projects",sa.Column("id",sa.String,primary_key=True),
        sa.Column("name",sa.String,nullable=False),sa.Column("state",sa.String,nullable=False),sa.Column("district",sa.String,nullable=False),
        sa.Column("locality",sa.String),sa.Column("ward_village",sa.String),sa.Column("category",sa.String,nullable=False),
        sa.Column("location",Geometry("POINT",srid=4326),nullable=False),sa.Column("department",sa.String),
        sa.Column("contractor",sa.String),sa.Column("sanctioned_cost",sa.Float),sa.Column("actual_cost",sa.Float),
        sa.Column("planned_start",sa.DateTime(timezone=True)),sa.Column("planned_completion",sa.DateTime(timezone=True)),
        sa.Column("actual_start",sa.DateTime(timezone=True)),sa.Column("actual_completion",sa.DateTime(timezone=True)),
        sa.Column("responsible_agency",sa.String),sa.Column("responsible_official",sa.String),sa.Column("office_contact",sa.String),
        sa.Column("department_chain",sa.String),sa.Column("status",sa.String,nullable=False),sa.Column("progress",sa.Integer,nullable=False),
        sa.Column("source_badges",sa.JSON,nullable=False),sa.Column("is_sample",sa.Boolean,nullable=False))
    op.create_table("project_timeline_events",sa.Column("id",sa.String,primary_key=True),
        sa.Column("project_id",sa.String,sa.ForeignKey("projects.id"),nullable=False),
        sa.Column("stage",sa.String,nullable=False),sa.Column("occurred_at",sa.DateTime(timezone=True),nullable=False))
    op.create_table("integrations_status",sa.Column("name",sa.String,primary_key=True),
        sa.Column("status",sa.String,nullable=False),sa.CheckConstraint("status IN ('not_connected','planned')",name="integration_honesty"))
    for name in ["pfms","iig","esakshi","pmgsy_gis","cpgrams","state_edistrict","csc","depa"]:
        op.execute(sa.text("INSERT INTO integrations_status(name,status) VALUES (:n,'planned')").bindparams(n=name))
def downgrade():
    raise RuntimeError("Destructive downgrade disabled.")
