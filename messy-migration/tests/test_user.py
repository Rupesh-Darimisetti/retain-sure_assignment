import pytest
import requests

BASE_URL = 'http://localhost:5009'

# Shared test data
TEST_USER = {
    "name": "Pytest User",
    "email": "pytest@example.com",
    "password": "pytest123"
}
UPDATED_USER = {
    "name": "Pytest User Updated",
    "email": "updated_pytest@example.com"
}

@pytest.fixture(scope="module")
def create_user():
    # Create user
    res = requests.post(f"{BASE_URL}/users", json=TEST_USER)
    assert res.status_code == 201

    # Fetch all users to get the new user's ID
    res = requests.get(f"{BASE_URL}/users")
    assert res.status_code == 200
    users = res.json()
    print(users)
    user_id = None
    for user in users:
        if user[1] == TEST_USER["name"]:
            user_id = user[0]
            break

    assert user_id is not None
    yield user_id

    # Cleanup: Delete the user after tests
    res = requests.delete(f"{BASE_URL}/user/{user_id}")
    assert res.status_code == 200

def test_home():
    res = requests.get(f"{BASE_URL}/")
    assert res.status_code == 200
    assert "User Management System" in res.text

def test_get_all_users():
    res = requests.get(f"{BASE_URL}/users")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_get_user(create_user):
    user_id = create_user
    res = requests.get(f"{BASE_URL}/users/{user_id}")
    assert res.status_code == 200
    data = res.json()
    assert data[1] == TEST_USER["name"]

def test_update_user(create_user):
    user_id = create_user
    res = requests.put(f"{BASE_URL}/user/{user_id}", json=UPDATED_USER)
    assert res.status_code == 200
    assert "User updated" in res.text

def test_search_user():
    res = requests.get(f"{BASE_URL}/search", params={"name": "Pytest"})
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_login():
    res = requests.post(f"{BASE_URL}/login", json={
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    })
    assert res.status_code == 200
    json_data = res.json()
    assert "status" in json_data
    assert json_data["status"] in ["success", "failed"]

def test_delete_user_independent():
    # Create a separate user for delete test
    res = requests.post(f"{BASE_URL}/users", json={
        "name": "ToDelete",
        "email": "delete_me@example.com",
        "password": "delete123"
    })
    assert res.status_code == 201

    # Fetch the ID
    users = requests.get(f"{BASE_URL}/users").json()
    user_id = next(u[0] for u in users if u[1] == "ToDelete")

    # Delete
    res = requests.delete(f"{BASE_URL}/user/{user_id}")
    assert res.status_code == 200
