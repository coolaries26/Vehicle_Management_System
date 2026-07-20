from sqlalchemy import text
from app.db.session import engine

def test_db_connection():
    with engine.connect() as conn:
        result = conn.execute(
            text("select current_database()")
        )

        db = result.scalar()

        assert db == "fms"