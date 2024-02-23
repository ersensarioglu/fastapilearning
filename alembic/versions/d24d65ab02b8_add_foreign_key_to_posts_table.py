"""add foreign-key to posts table

Revision ID: d24d65ab02b8
Revises: 0c9712773e7e
Create Date: 2024-02-23 17:37:34.663381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd24d65ab02b8'
down_revision: Union[str, None] = '0c9712773e7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('created_by', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', local_cols=['created_by'], remote_cols=['id'], ondelete='CASCADE')
    pass

def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'created_by')
    pass
