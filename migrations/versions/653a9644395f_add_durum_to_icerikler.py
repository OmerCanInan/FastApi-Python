"""add durum to icerikler

Revision ID: 653a9644395f
Revises: 8a12d5201351
Create Date: 2026-11-23 10:15:12.525828

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '653a9644395f'
down_revision: Union[str, Sequence[str], None] = '8a12d5201351'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE icerikler
        ADD COLUMN durum TEXT NOT NULL DEFAULT 'taslak'
        CHECK (durum IN ('taslak', 'onaylandi', 'yayinlandi'))
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        ALTER TABLE icerikler
        DROP COLUMN durum
    """)
