# Tests automatisés de l'app FastAPI.
# TestClient simule des requêtes HTTP vers l'app SANS démarrer de vrai
# serveur ni toucher au réseau. Rapide et isolé.
import psycopg
import pytest
from fastapi.testclient import TestClient

from main import app, DB_DSN

client = TestClient(app)


def test_root_repond_200():
    # GET / doit renvoyer 200 et le message de bienvenue.
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Salut depuis l'app conteneurisee"}


def test_health_repond_ok():
    # GET /health doit renvoyer 200 et le statut "ok". Ne touche pas la base.
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def _db_reachable():
    # Sonde rapide : la base est-elle joignable ? (2 s max)
    try:
        with psycopg.connect(DB_DSN, connect_timeout=2):
            return True
    except Exception:
        return False


# Ce test ne tourne QUE si une base est disponible. En local sans base il se
# saute (pas d'échec) ; en CI, le service Postgres le rend joignable.
@pytest.mark.skipif(
    not _db_reachable(),
    reason="Postgres indisponible : test joue uniquement en CI",
)
def test_db_reachable():
    response = client.get("/db")
    assert response.status_code == 200
    assert response.json()["database"] == "reachable"
