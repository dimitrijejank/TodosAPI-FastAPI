from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
import pytest
from models import Todos, Users
from fastapi import status
import os
from dotenv import load_dotenv
from routers.users import bcrypt_context

load_dotenv()

SQLALCEHEMY_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(SQLALCEHEMY_URL)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username": "dimitrije", "id": 1, "user_role": "admin"}

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture()
def test_user():
    user = Users(
        id = 1,
        email="dimitrije@gmail.com",
        username="dimitrije",
        first_name="dimitrije",
        last_name="jankovic",
        role="admin",
        hashed_password=bcrypt_context.hash("testpassword"),
        is_active=True,
        phone_number="1111111111111"
    )
    db =TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    db.query(Users).filter(Users.id == user.id).delete()
    db.commit()
    db.close()

@pytest.fixture
def test_todo(test_user):
    todo = Todos(
        title="Learn python",
        description="Watch daily course on udemy",
        priority=4,
        complete=False,
        owner_id=test_user.id
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    # with engine.connect() as connection:
    #     connection.execute(text("DELETE FROM todos;"))
    #     connection.commit()
    db.query(Todos).filter(Todos.id == todo.id).delete()
    db.commit()
    db.close()