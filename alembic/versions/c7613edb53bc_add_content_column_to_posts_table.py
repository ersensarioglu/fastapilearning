"""add content column to posts table

Revision ID: c7613edb53bc
Revises: 8ecba173f2d5
Create Date: 2024-02-23 17:20:46.519335

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7613edb53bc'
down_revision: Union[str, None] = '8ecba173f2d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
