from fastapi import FastAPI
from .db import Base, engine
from .models import Item, Movement, User
from .deps import setup_cors
from .routers import items, movements, auth as auth_router

app = FastAPI(title="Inventory API")
setup_cors(app)

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth_router.router)
app.include_router(items.router)
app.include_router(movements.router)
