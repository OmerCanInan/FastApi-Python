"""add text search column to parcalar

Revision ID: 7a0eeac918b6
Revises: c5d8692148d5
Create Date: 2026-11-27 11:46:16.893198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a0eeac918b6'
down_revision: Union[str, Sequence[str], None] = 'c5d8692148d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        ALTER TABLE parcalar
        ADD COLUMN arama tsvector
        GENERATED ALWAYS AS (to_tsvector('turkish', metin)) STORED
    """)
    op.execute("CREATE INDEX parcalar_arama_idx ON parcalar USING gin (arama)")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX parcalar_arama_idx")
    op.execute("ALTER TABLE parcalar DROP COLUMN arama")