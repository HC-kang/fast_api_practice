"""create phone number for user col

Revision ID: 876b6699e641
Revises: 
Create Date: 2022-09-04 15:08:29.776523

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '876b6699e641'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column('phone_number', sa.String(), nullable=True))


def downgrade():
    op.drop_column("users", "phone_number")
