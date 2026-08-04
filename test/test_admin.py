from .utils import *
from routers.admin import get_current_user,get_db

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo, test_user):
    response = client.get("/admin/todo")
    assert response.status_code ==status.HTTP_200_OK
    assert response.json() == [{"id":test_todo.id,
                                "title": "Learn python",
                                "description": "Watch daily course on udemy",
                                "priority": 4,
                                "complete": False,
                                "owner_id": test_user.id}]
def test_admin_delete_todo(test_todo):
    response = client.delete(f"/admin/todo/{test_todo.id}")
    assert response.status_code == 204

    db = TestingSessionLocal()
    deleted_todo  = db.query(Todos).filter(Todos.id == test_todo.id).first()
    assert deleted_todo is None

def test_admin_delete_todo_not_found(test_todo,test_user):
    response = client.delete("admin/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}