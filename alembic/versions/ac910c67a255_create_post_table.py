"""create post table

Revision ID: ac910c67a255
Revises: 
Create Date: 2023-12-10 20:59:39.557495

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ac910c67a255'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("Substances",sa.Column("id", sa.Integer(), nullable=False,primary_key= True)
                                ,sa.Column("name", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_table("Substances")
    pass
