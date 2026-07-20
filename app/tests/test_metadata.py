# tests/test_metadata.py

from app.db.base import Base
from app.models import *
import app.models

def test_metadata_loads():
    print(Base.metadata.tables.keys())
    assert len(Base.metadata.tables) > 0