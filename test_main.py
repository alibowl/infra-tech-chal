import pytest
from fastapi.testclient import TestClient
from requests.exceptions import RequestException

from main import app


client = TestClient(app)


def test_root_form_page():
    """Test GET / returns the HTML form."""
    response = client.get("/")
    assert response.status_code == 200
    assert "<h1>Enter a Pokémon Name</h1>" in response.text
    assert "<form action=\"/pokemon\" method=\"post\">" in response.text


def test_get_pokemon_success(monkeypatch):
    """Test POST /pokemon with a valid Pokémon name."""

    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "name": "pikachu",
                "id": 25,
                "height": 4,
                "weight": 60,
                "types": [
                    {"type": {"name": "electric"}}
                ],
                "abilities": [
                    {"ability": {"name": "static"}},
                    {"ability": {"name": "lightning-rod"}},
                ],
            }

    def mock_get(url):
        return MockResponse()

    monkeypatch.setattr("main.requests.get", mock_get)

    response = client.post(
        "/pokemon",
        data={"pokemon_name": "Pikachu"},
    )

    assert response.status_code == 200
    assert "<h1>Pikachu Stats</h1>" in response.text
    assert "<td>25</td>" in response.text
    assert "<td>Electric</td>" in response.text
    assert "Static" in response.text
    assert "Lightning-Rod" in response.text


def test_get_pokemon_not_found(monkeypatch):
    """Test POST /pokemon when the Pokémon is not found."""

    def mock_get(url):
        raise Req
