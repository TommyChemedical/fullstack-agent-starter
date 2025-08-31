from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.src.main import app
from app.src.models.base import Base
from app.src.core.database import get_session

# In-Memory-DB nur für Tests
engine = create_engine("sqlite+pysqlite:///:memory:", future=True, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base.metadata.create_all(bind=engine)

def override_get_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_session] = override_get_session

def test_create_and_list_course():
    client = TestClient(app)
    r = client.post("/api/courses", json={"title": "Math 101", "description": "Intro"})
    assert r.status_code == 201
    item = r.json()
    assert item["id"] == 1
    assert item["title"] == "Math 101"

    r2 = client.get("/api/courses")
    assert r2.status_code == 200
    items = r2.json()
    assert len(items) == 1
    assert items[0]["title"] == "Math 101"
