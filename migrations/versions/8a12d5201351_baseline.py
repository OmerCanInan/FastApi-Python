"""baseline

Revision ID: 8a12d5201351
Revises: 
Create Date: 2026-11-23 09:52:41.583055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a12d5201351'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE TABLE icerikler (
            id         SERIAL PRIMARY KEY,
            baslik     TEXT NOT NULL,
            platform   TEXT NOT NULL,
            adet       INTEGER NOT NULL DEFAULT 1 CHECK (adet BETWEEN 1 AND 10),
            olusturma  TIMESTAMPTZ NOT NULL DEFAULT now()
        )
    """)
    op.execute("""
        CREATE TABLE dosyalar (
            id             SERIAL PRIMARY KEY,
            ad             TEXT NOT NULL,
            tur            TEXT,
            boyut          INTEGER NOT NULL,
            hash           TEXT NOT NULL UNIQUE,
            yuklenme       TIMESTAMPTZ NOT NULL DEFAULT now(),
            depo_anahtari  TEXT
        )
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP TABLE dosyalar")
    op.execute("DROP TABLE icerikler")
