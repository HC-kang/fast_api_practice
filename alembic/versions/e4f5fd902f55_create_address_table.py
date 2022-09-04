"""create address table

Revision ID: e4f5fd902f55
Revises: 876b6699e641
Create Date: 2022-09-04 15:30:25.866277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4f5fd902f55'
down_revision = '876b6699e641'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("address",
                    sa.Column('id', sa.Integer(), nullable=True, primary_key=True),
                    sa.Column('address1', sa.String(), nullable=False),
                    sa.Column('address2', sa.String(), nullable=False),
                    sa.Column('city', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('country', sa.String(), nullable=False),
                    sa.Column('postalcode', sa.String(), nullable=False)
                    )


def downgrade():
    op.drop_table('address')
