import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from app.database import Base
from app.config import settings
import app.models

from urllib.parse import urlparse, parse_qs, urlencode

_connect_args_from_url = {}

current_db_url = settings.database_url
parsed_url = urlparse(current_db_url)
query_params = parse_qs(parsed_url.query)

if 'sslmode' in query_params:
    sslmode_value = query_params.pop('sslmode')[0]

    if sslmode_value == 'require':
        _connect_args_from_url['ssl'] = True

query_params.pop('channel_binding', None)

new_query_string = urlencode(query_params, doseq=True)
cleaned_db_url = parsed_url._replace(query=new_query_string).geturl()

config = context.config
config.set_main_option("sqlalchemy.url", cleaned_db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
    
async def run_migrations_online() -> None:

    connect_params = config.get_section(config.config_ini_section, {})
    
    if _connect_args_from_url:
        connect_params['connect_args'] = _connect_args_from_url

    connectable = async_engine_from_config(
        connect_params,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
