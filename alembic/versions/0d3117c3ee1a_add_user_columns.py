"""Add User Columns

Revision ID: 0d3117c3ee1a
Revises: 1982c4cb8efb
Create Date: 2024-06-01 09:52:09.662819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d3117c3ee1a'
down_revision: Union[str, None] = '1982c4cb8efb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable= False, server_default="True"))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable= False, server_default= 'now()'))
    pass


def downgrade() -> None:
    op.drop_column('posts',"published")
    op.drop_column('posts',"created_at")
    pass
