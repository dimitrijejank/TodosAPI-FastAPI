from fastapi import status
from .utils import *

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db

def test_read_all_autheticated(test_todo,test_user):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"id": test_todo.id,
                                "title": "Learn python",
                                "description": "Watch daily course on udemy",
                                "priority": 4,
                                "complete": False,
                                "owner_id": test_user.id}]

def test_read_one_authenticated(test_todo):
    response = client.get(f"/{test_todo.id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == test_todo.title
    assert response.json()["description"] == test_todo.description

def test_read_one_authenticated_not_found():
    response = client.get("/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

def test_create_todo(test_todo,test_user):
    request_data = {
        "title": "New todo",
        "description": "New todo description",
        "priority": 5,
        "complete": False,
        "owner_id": test_user.id
    }

    response = client.post("/todo", json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    created_todo = db.query(Todos).filter(Todos.title == "New todo").first()
    db.query(Todos).filter(Todos.id == created_todo.id).delete()
    db.commit()
    db.close()

def test_update_todo(test_todo, test_user):
    request_data = {
        "title": "Changed title",
        "description": "Need to learn testing",
        "priority": 5,
        "complete": False,
        "owner_id": test_user.id
    }

    response = client.put(f"/todo/{test_todo.id}", json=request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    updated_todo = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert updated_todo.title == "Changed title"

def test_update_todo_not_found(test_todo,test_user):
    request_data = {
        "title": "Changed title",
        "description": "Need to learn testing",
        "priority": 5,
        "complete": False,
        "owner_id": test_user.id
    }

    response = client.put("/todo/999",json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

def test_delete_todo(test_todo,test_user):
    response = client.delete(f"/todo/{test_todo.id}")
    assert response.status_code == 204
    db = TestingSessionLocal()
    deleted_todo = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert deleted_todo is None

def test_delete_todo_not_found(test_todo,test_user):
    response = client.delete(f"/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
