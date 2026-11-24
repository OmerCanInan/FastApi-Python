"""add hnsw index on parcalar embedding

Revision ID: c5d8692148d5
Revises: be61cf689222
Create Date: 2026-11-24 14:21:47.909337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5d8692148d5'
down_revision: Union[str, Sequence[str], None] = 'be61cf689222'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "CREATE INDEX parcalar_embedding_idx ON parcalar "
        "USING hnsw (embedding vector_cosine_ops)"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DROP INDEX parcalar_embedding_idx")