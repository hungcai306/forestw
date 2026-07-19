from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings

class Base(DeclarativeBase):
    pass

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def _migrate_username(conn) -> None:
    """Migration nhẹ để các database Render cũ chuyển từ email sang admin_username."""
    conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS admin_username VARCHAR(80)'))
    conn.execute(text("""
        UPDATE users
        SET admin_username = LOWER(
            REGEXP_REPLACE(
                COALESCE(NULLIF(SPLIT_PART(email, '@', 1), ''), 'user_' || id::text),
                '[^a-zA-Z0-9_.]+', '_', 'g'
            )
        )
        WHERE admin_username IS NULL OR admin_username = ''
    """))
    conn.execute(text('ALTER TABLE users ALTER COLUMN admin_username SET NOT NULL'))
    conn.execute(text('ALTER TABLE users ALTER COLUMN email DROP NOT NULL'))
    conn.execute(text('CREATE UNIQUE INDEX IF NOT EXISTS ix_users_admin_username ON users (admin_username)'))

def init_database() -> None:
    from app.models import entities  # noqa: F401
    with engine.begin() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        _migrate_username(conn)
