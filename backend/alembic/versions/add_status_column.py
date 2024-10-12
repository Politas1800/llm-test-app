"""add status column

Revision ID: add_status_column
Revises: 8d687fbc519f
Create Date: 2024-10-12 15:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_status_column'
down_revision = 'c07987c701a7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tests', sa.Column('status', sa.String(), nullable=True))


def downgrade():
    op.drop_column('tests', 'status')
