"""Add users and recipe table

Revision ID: 9d7f6ae090a0
Revises: 
Create Date: 2022-09-14 08:00:23.336301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d7f6ae090a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('hashed_password', sa.String(length=256), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('phone', sa.String(length=256), nullable=True),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('credit_point', sa.Integer(), nullable=False),
    sa.Column('free_point', sa.Integer(), nullable=False),
    sa.Column('business_class', sa.String(length=256), nullable=True),
    sa.Column('business_name', sa.String(length=256), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('is_notification', sa.Boolean(), nullable=True),
    sa.Column('business_president', sa.String(length=256), nullable=True),
    sa.Column('approve_status_flag', sa.Enum('W', 'A', 'D', 'S', name='userapprovestatusflag'), nullable=True),
    sa.Column('is_superuser', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=256), nullable=False),
    sa.Column('url', sa.String(length=256), nullable=True),
    sa.Column('source', sa.String(length=256), nullable=True),
    sa.Column('submitter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['submitter_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_recipes_id'), 'recipes', ['id'], unique=False)
    op.create_index(op.f('ix_recipes_url'), 'recipes', ['url'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_recipes_url'), table_name='recipes')
    op.drop_index(op.f('ix_recipes_id'), table_name='recipes')
    op.drop_table('recipes')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
