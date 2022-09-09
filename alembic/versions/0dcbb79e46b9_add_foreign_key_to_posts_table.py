"""add foreign-key to posts table

Revision ID: 0dcbb79e46b9
Revises: 3bdf0905c0b1
Create Date: 2022-09-08 21:29:35.022148

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0dcbb79e46b9'
down_revision = '3bdf0905c0b1'
branch_labels = None
depends_on = None

#Note that we first have to add a column to the posts table called owner_id- to be able to match with users.
def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))        
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")    

#Drop then constraint first, then the column.
def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
