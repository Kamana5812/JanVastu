"""Preserve supplied dataset claims without inventing location or progress."""
from alembic import op
import sqlalchemy as sa

revision="0008"
down_revision="0007"
branch_labels=None
depends_on=None

def upgrade():
    op.alter_column("projects","location",nullable=True)
    op.alter_column("projects","progress",nullable=True,server_default=None)
    op.add_column("projects",sa.Column("dataset_record",sa.JSON(),nullable=True))

def downgrade():
    # Refuse data loss: records with unknown values cannot satisfy the old schema.
    op.alter_column("projects","location",nullable=False)
    op.alter_column("projects","progress",nullable=False)
    op.drop_column("projects","dataset_record")
