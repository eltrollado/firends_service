import databases
import sqlalchemy

from app.config import settings

DATABASE_URL = f'postgresql://{settings.db_user}:{settings.db_pass}@{settings.db_url}/{settings.db_name}'

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

friends = sqlalchemy.Table(
    "friends",
    metadata,
    sqlalchemy.Column("user", sqlalchemy.Integer, index=True),
    sqlalchemy.Column("friend", sqlalchemy.Integer),
    sqlalchemy.UniqueConstraint('user', 'friend', name='uix_1')
)


engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={}
)

metadata.create_all(engine)
