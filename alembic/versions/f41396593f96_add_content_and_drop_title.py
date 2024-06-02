"""Add content and drop Title

Revision ID: f41396593f96
Revises: 126f1a3558cf
Create Date: 2024-06-01 08:51:21.072110

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f41396593f96'
down_revision: Union[str, None] = '126f1a3558cf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable= False))
    op.drop_column('posts', 'title')
    op.add_column('posts', sa.Column('title', sa.String(), nullable= False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    op.add_column('posts',  sa.Column('title', sa.Integer(), nullable= False))
    op.drop_column("posts", "title")
   
    pass
