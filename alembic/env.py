from logging.config import fileConfig

from sqlalchemy import engine_from_config, URL, create_engine
from sqlalchemy import pool

from alembic import context
from app.db.base import Base
import app.models


from urllib.parse import quote_plus


from app.core.config import get_settings

settings = get_settings()
pwd = quote_plus(settings.DB_PASSWORD)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config


# DATABASE_URL = URL.create(
#     drivername="postgresql+psycopg2",
#     username=settings.DB_USER,
#     password="FleetUser@2024!",
#     host=settings.DB_HOST,
#     port=settings.DB_PORT,
#     database=settings.DB_NAME,
# )
# 
# print("=" * 50)
# print("DATABASE_URL =", DATABASE_URL)
# 
# engine = create_engine(DATABASE_URL)
# 
# try:
#     with engine.connect() as conn:
#         print("SQLAlchemy connection SUCCESS")
# except Exception as e:
#     print("SQLAlchemy connection FAILED")
#     print(type(e))
#     print(e)
#     raise
# print("=" * 50)
# 
# 
# config.set_main_option(
#     "sqlalchemy.url",
#     str(DATABASE_URL).replace("%", "%%")
# )
# 
# print("=" * 50)
# print("USER     :", repr(settings.DB_USER))
# print("PASSWORD :", repr(settings.DB_PASSWORD))
# print("HOST     :", repr(settings.DB_HOST))
# print("PORT     :", repr(settings.DB_PORT))
# print("DB       :", repr(settings.DB_NAME))
# print("=" * 50)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
#target_metadata = None
target_metadata = Base.metadata
# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    print("=" * 50)

    print("=" * 50)

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
