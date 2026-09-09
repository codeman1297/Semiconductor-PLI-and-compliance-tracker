import os
os.environ['DATABASE_URL']='sqlite:///./test_tracker.db'
os.environ['ADMIN_API_KEY']='test-key'
import pytest
from fastapi.testclient import TestClient
from app.db.base import Base
from app.db.session import engine
from app.main import app
@pytest.fixture(autouse=True)
def database():
 Base.metadata.drop_all(engine); Base.metadata.create_all(engine); yield; Base.metadata.drop_all(engine)
@pytest.fixture
def client(): return TestClient(app)
@pytest.fixture
def payload(): return {"project_name":"Test Fab","company_name":"Test Semiconductor","state":"Gujarat","project_type":"Semiconductor Fab","status":"APPROVED","publication_status":"PUBLISHED","announcement_date":"2024-01-01","sources":[{"source_type":"PIB","publisher":"PIB","title":"Approval","url":"https://example.gov/approval","reliability":"HIGH"}]}
