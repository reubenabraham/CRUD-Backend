"""add content column to posts table

Revision ID: 7aadeefbdc91
Revises: f94d8b997c64
Create Date: 2022-09-08 17:42:58.624507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7aadeefbdc91'
down_revision = 'f94d8b997c64'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
