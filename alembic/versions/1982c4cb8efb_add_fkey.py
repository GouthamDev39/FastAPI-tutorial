"""Add fkey

Revision ID: 1982c4cb8efb
Revises: d571b80611d1
Create Date: 2024-06-01 09:43:16.124411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1982c4cb8efb'
down_revision: Union[str, None] = 'd571b80611d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column("user_id", sa.Integer(), nullable= False))
    op.create_foreign_key('post_user_fk', source_table = "posts", referent_table = "users",
                          local_cols = ['user_id'], remote_cols = ['id'], ondelete = "CASCADE")


def downgrade() -> None:
    op.drop_constrainst('post_user_fk', table_name = "posts")
    op.drop_column("posts", "user_id")
    pass
