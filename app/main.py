from fastapi import FastAPI

from app.core.config import APP_NAME, APP_VERSION
from app.db.database import Base, engine
from app.routers.tickets import router as tickets_router

app = FastAPI(title=APP_NAME, version=APP_VERSION)
app.include_router(tickets_router)
Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"name": APP_NAME, "status": "running", "version": APP_VERSION}
