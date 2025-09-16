from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_post_spent():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["Hello"] == "World"


def test_metadata():
    assert app.description == "API made by NIES"
    assert app.title == "API of NIES"
    assert app.summary == "API about data of using by NIES"
    assert app.version == "0.1.0"
    contact = {
        "name": "NIES",
        "url": "https://github.com/niesfutbol",
        "email": "nepo@nies.futbol",
    }
    assert app.contact == contact
    license_info = {
        "name": "AGPL-3.0 license",
        "url": "https://github.com/niesfutbol/api_nies/blob/develop/LICENSE",
    }
    assert app.license_info == license_info
