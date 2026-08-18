"""add device_type to refresh_tokens

Revision ID: a3c9d2f1e7b4
Revises: 1f0bdb6e18d6
Create Date: 2026-08-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a3c9d2f1e7b4'
down_revision: Union[str, Sequence[str], None] = '1f0bdb6e18d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'refresh_tokens',
        sa.Column('device_type', sa.String(length=30), nullable=True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('refresh_tokens', 'device_type')
