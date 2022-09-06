"""create apt_num to address

Revision ID: 27a184a66110
Revises: 06b107492e9e
Create Date: 2022-09-04 16:37:15.637785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '27a184a66110'
down_revision = '06b107492e9e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("address", sa.Column('apt_num', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('address', 'apt_num')
