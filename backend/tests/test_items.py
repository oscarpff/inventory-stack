import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import SessionLocal
from app.models import User
from app.auth import get_password_hash

client = TestClient(app)

def get_token():
    # ensure user exists
    db = SessionLocal()
    if not db.query(User).filter(User.username=="admin").first():
        db.add(User(username="admin", hashed_password=get_password_hash("admin123")))
        db.commit()
    db.close()
    resp = client.post("/auth/token", data={"username":"admin","password":"admin123"})
    assert resp.status_code == 200
    return resp.json()["access_token"]

def test_list_items():
    r = client.get("/items")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_update_quantity_and_movement():
    token = get_token()
    # assume item 1 exists from seed or creation on test start; if not, skip gracefully
    items = client.get("/items").json()
    if not items:
        pytest.skip("No items to test")
    first_id = items[0]["id"]
    current_qty = items[0]["quantity"]
    new_qty = current_qty + 5
    r = client.patch(f"/items/{first_id}/quantity", json={"quantity": new_qty, "reason": "test add"}, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200
    assert r.json()["quantity"] == new_qty
    # check movements
    m = client.get("/movements?limit=5").json()
    assert any(x["delta"] == 5 and x["item_id"] == first_id for x in m)
