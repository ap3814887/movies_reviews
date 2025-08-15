"""добавлен столбец sentiment в reviews

Revision ID: 2c153b20aa93
Revises: migration_lvl1
Create Date: 2025-08-12 17:18:10.064047

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "migration_lvl2"
down_revision: Union[str, Sequence[str], None] = "migration_lvl1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # создаём ENUM тип вручную
    sentiment_enum = sa.Enum('positive', 'neutral', 'negative', name='sentimentenum')
    sentiment_enum.create(op.get_bind(), checkfirst=True)

    # добавляем колонку
    op.add_column(
        "reviews",
        sa.Column(
            "sentiment",
            sentiment_enum,
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("reviews", "sentiment")

    # удаляем ENUM
    sentiment_enum = sa.Enum('positive', 'neutral', 'negative', name='sentimentenum')
    sentiment_enum.drop(op.get_bind(), checkfirst=True)