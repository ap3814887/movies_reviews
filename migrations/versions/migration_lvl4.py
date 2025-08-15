"""seed test data

Revision ID: migration_lvl4
Revises: migration_lvl3
Create Date: 2025-08-13 21:22:32.962287
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from datetime import datetime
from app.sentiment_types import SentimentEnum
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# revision identifiers, used by Alembic.
revision: str = "migration_lvl4"
down_revision: Union[str, Sequence[str], None] = "migration_lvl3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    conn = op.get_bind()

    # 1. Пользователи с нормальными тестовыми паролями
    users = [
        ("Иван Петров", "ivan@example.com", pwd_context.hash("password1")),
        ("Мария Смирнова", "maria@example.com", pwd_context.hash("password2")),
        ("Алексей Кузнецов", "alex@example.com", pwd_context.hash("password3")),
    ]
    for name, email, password in users:
        conn.execute(sa.text("""
            INSERT INTO users (name, email, hashed_password)
            VALUES (:name, :email, :password)
        """), {"name": name, "email": email, "password": password})

    # 2. Фильмы и отзывы
    movies_data = [
        [
            ("Титаник", 10, "Фильм заставил меня плакать!", SentimentEnum.positive),
            ("Интерстеллар", 9, "Впечатляюще и философски.", SentimentEnum.positive),
            ("Мстители: Финал", 8, "Сильно, но ожидал большего.", SentimentEnum.neutral),
            ("Хатико", 10, "Нереально трогательная история.", SentimentEnum.positive),
            ("Джокер", 7, "Сильная игра актёра, но слишком мрачно.", SentimentEnum.negative),
        ],
        [
            ("Начало", 9, "Очень закрученный сюжет!", SentimentEnum.positive),
            ("Побег из Шоушенка", 10, "Лучший фильм, что я видел.", SentimentEnum.positive),
            ("Матрица", 8, "Визуал потрясающий, но немного устарел.", SentimentEnum.neutral),
            ("1+1", 9, "Фильм, который учит ценить жизнь.", SentimentEnum.positive),
            ("Гравитация", 7, "Напряжённо, но одноразово.", SentimentEnum.neutral),
        ],
        [
            ("Форрест Гамп", 10, "Смотрю уже 5-й раз!", SentimentEnum.positive),
            ("Бойцовский клуб", 9, "Финал взорвал мозг!", SentimentEnum.positive),
            ("Властелин колец: Братство Кольца", 10, "Легендарная история.", SentimentEnum.positive),
            ("Темный рыцарь", 8, "Сильный злодей, но затянуто.", SentimentEnum.neutral),
            ("Гладиатор", 9, "Вдохновляющая история.", SentimentEnum.positive),
        ],
    ]

    movie_id_counter = 1
    for user_id, movie_list in enumerate(movies_data, start=1):
        for title, rating, review_text, sentiment in movie_list:
            conn.execute(sa.text("""
                INSERT INTO movies (title, created_at)
                VALUES (:title, :created_at)
            """), {"title": title, "created_at": datetime.now()})

            conn.execute(sa.text("""
                INSERT INTO reviews (movie_id, user_id, rating, review_text, sentiment, created_at)
                VALUES (:movie_id, :user_id, :rating, :review_text, :sentiment, :created_at)
            """), {
                "movie_id": movie_id_counter,
                "user_id": user_id,
                "rating": rating,
                "review_text": review_text,
                "sentiment": sentiment.value,
                "created_at": datetime.now()
            })

            movie_id_counter += 1


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("""
        DELETE FROM reviews
        WHERE review_text IN (
            'Фильм заставил меня плакать!',
            'Впечатляюще и философски.',
            'Сильно, но ожидал большего.',
            'Нереально трогательная история.',
            'Сильная игра актёра, но слишком мрачно.',
            'Очень закрученный сюжет!',
            'Лучший фильм, что я видел.',
            'Визуал потрясающий, но немного устарел.',
            'Фильм, который учит ценить жизнь.',
            'Напряжённо, но одноразово.',
            'Смотрю уже 5-й раз!',
            'Финал взорвал мозг!',
            'Легендарная история.',
            'Сильный злодей, но затянуто.',
            'Вдохновляющая история.'
        )
    """))
    conn.execute(sa.text("""
        DELETE FROM movies
        WHERE title IN (
            'Титаник','Интерстеллар','Мстители: Финал','Хатико','Джокер',
            'Начало','Побег из Шоушенка','Матрица','1+1','Гравитация',
            'Форрест Гамп','Бойцовский клуб','Властелин колец: Братство Кольца',
            'Темный рыцарь','Гладиатор'
        )
    """))
    conn.execute(sa.text("""
        DELETE FROM users
        WHERE email IN ('ivan@example.com','maria@example.com','alex@example.com')
    """))
