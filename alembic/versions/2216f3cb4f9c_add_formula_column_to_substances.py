"""add formula column to substances 

Revision ID: 2216f3cb4f9c
Revises: ac910c67a255
Create Date: 2023-12-10 21:31:03.201689

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2216f3cb4f9c'
down_revision: Union[str, None] = 'ac910c67a255'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("Substances", sa.Column("formula", sa.String, nullable=False))


def downgrade() -> None:
    op.drop_column("Substances","formula")
    pass
