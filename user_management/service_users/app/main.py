from fastapi import FastAPI
from app.db.session import create_tables
from app.routes import users

app = FastAPI()

# Créer les tables lors du démarrage de l'application
@app.on_event("startup")
def on_startup():
    create_tables()

# Inclure les routes
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management Service"}
