"""add rank_all to verse

Revision ID: 0f76756e7424
Revises: 8db0bbec1d36
Create Date: 2024-10-18 15:36:25.898001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f76756e7424'
down_revision: Union[str, None] = '8db0bbec1d36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('verse', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rank_all', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('verse', schema=None) as batch_op:
        batch_op.drop_column('rank_all')

    # ### end Alembic commands ###
