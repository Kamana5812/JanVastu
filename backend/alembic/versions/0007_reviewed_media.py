"""Separate reviewed public derivatives from private originals."""
from alembic import op
import sqlalchemy as sa
revision="0007"
down_revision="0006"
branch_labels=None
depends_on=None
def upgrade():
    op.add_column("needs",sa.Column("is_sample",sa.Boolean(),server_default=sa.false(),nullable=False))
    op.add_column("evidence",sa.Column("public_file_url",sa.String(),nullable=True))
def downgrade():
    op.drop_column("needs","is_sample")
    op.drop_column("evidence","public_file_url")
