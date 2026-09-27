"""Keep verification notes private and attributable."""
from alembic import op
import sqlalchemy as sa
revision="0004"
down_revision="0003"
branch_labels=None
depends_on=None
def upgrade():
    op.create_table("moderation_notes",sa.Column("id",sa.String,primary_key=True),
        sa.Column("need_id",sa.String,sa.ForeignKey("needs.id"),nullable=False),
        sa.Column("actor_id",sa.String,sa.ForeignKey("users.id"),nullable=False),
        sa.Column("note",sa.String,nullable=False),sa.Column("created_at",sa.DateTime(timezone=True)))
def downgrade():
    raise RuntimeError("Destructive downgrade disabled.")
