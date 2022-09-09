"""add user table

Revision ID: 3bdf0905c0b1
Revises: 7aadeefbdc91
Create Date: 2022-09-08 21:19:03.944140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bdf0905c0b1'
down_revision = '7aadeefbdc91'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False), sa.Column('email', sa.String(), nullable=False), sa.Column('password', sa.String(), nullable=False), sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()') ,nullable=False), sa.PrimaryKeyConstraint('id'), sa.UniqueConstraint('email'))


def downgrade() -> None:
    op.drop_table('users')

    
