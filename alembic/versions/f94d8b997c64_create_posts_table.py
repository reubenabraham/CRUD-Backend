"""create posts table

Revision ID: f94d8b997c64
Revises: 
Create Date: 2022-09-08 17:11:34.227920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f94d8b997c64'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    


def downgrade() -> None:
    op.drop_table('posts')

