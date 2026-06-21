import os
import psycopg
from fastapi import FastAPI

app = FastAPI(title="DevSecOps Lab App")

# DSN = chaîne de connexion à Postgres, construite depuis l'environnement.
# 'db' est le NOM DU SERVICE Postgres dans docker-compose : Docker le résout
# automatiquement en IP sur le réseau backend (DNS interne). On ne code donc
# jamais d'adresse IP en dur.
DB_DSN = (
    f"host={os.getenv('POSTGRES_HOST', 'db')} "
    f"dbname={os.getenv('POSTGRES_DB', 'app')} "
    f"user={os.getenv('POSTGRES_USER', 'app')} "
    f"password={os.getenv('POSTGRES_PASSWORD', '')}"
)


@app.get("/health")
def health():
    # Point de santé : utilisé plus tard par le reverse proxy et le monitoring
    # pour savoir si l'app est vivante. Ne touche pas la base exprès.
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Salut depuis l'app deployee automatiquement !"}


@app.get("/db")
def db_check():
    # Ouvre une connexion à Postgres et lit sa version.
    # Si ça répond, c'est que l'app atteint la base sur le réseau backend.
    with psycopg.connect(DB_DSN, connect_timeout=5) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
    return {"database": "reachable", "version": version}
