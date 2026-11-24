"""add parcalar table with pgvector

Revision ID: be61cf689222
Revises: 653a9644395f
Create Date: 2026-11-24 13:56:41.384010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'be61cf689222'
down_revision: Union[str, Sequence[str], None] = '653a9644395f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("""
        CREATE TABLE parcalar (
            id         SERIAL PRIMARY KEY,
            kaynak     TEXT NOT NULL,
            sira       INTEGER NOT NULL,
            metin      TEXT NOT NULL,
            embedding  VECTOR(1024) NOT NULL,
            olusturma  TIMESTAMPTZ NOT NULL DEFAULT now(),
            UNIQUE (kaynak, sira)
        )
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE parcalar")
