from fastapi import FastAPI
from contextlib import asynccontextmanager
from .api.websocket import router as ws_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (e.g., connect to DB)
    yield
    # Shutdown logic

app = FastAPI(
    title="NovaShell API",
    description="Backend for the NovaShell AI Assistant",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ws_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the NovaShell OS Backend API. Systems are online."}

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "NovaShell API"}
