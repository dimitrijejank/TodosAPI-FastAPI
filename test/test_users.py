from httpcore2 import request

from .utils import *
from routers.users import get_current_user,get_db

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json()["username"] == "dimitrije"
    assert response.json()["email"] == "dimitrije@gmail.com"
    assert response.json()["role"] == "admin"
    assert response.json()["first_name"] == "dimitrije"
    assert response.json()["last_name"] == "jankovic"
    assert response.json()["is_active"] == True
    assert response.json()["phone_number"] == "1111111111111"
    assert bcrypt_context.verify("testpassword", response.json()["hashed_password"])

def test_user_change_password(test_user):
    response = client.put("/users/password", json={"password": "testpassword",
                                                   "new_password": "newtestpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db = TestingSessionLocal()
    changed = db.query(Users).filter(Users.id == test_user.id).first()
    assert bcrypt_context.verify("newtestpassword",changed.hashed_password)

def test_user_change_password_invalid(test_user):
    response = client.put("/users/password", json={"password": "wrongpassword",
                                                   "new_password": "newpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Authentication failed"}

def test_change_user_phone_number(test_user):
    response = client.put("/users/phone_number", params={"phone_number": "0616805566"})
    assert response.status_code == status.HTTP_204_NO_CONTENT