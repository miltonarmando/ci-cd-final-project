import pytest
from app import app, db, Product

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_create_product(client):
    response = client.post("/products", json={
        "name": "Product1",
        "category": "Category1",
        "price": 99.99,
        "availability": True
    })
    assert response.status_code == 201
