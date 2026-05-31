"""FastAPI main application."""
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import SessionLocal, create_tables
from app.routers import game, roles, rooms, ws
from app.services import RoleService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting Werewolf Game API...")
    create_tables()
    logger.info("✅ Database tables created/verified")

    db = SessionLocal()
    try:
        RoleService.seed_roles(db)
        logger.info("✅ Default roles seeded/verified")
    finally:
        db.close()

    yield
    logger.info("🛑 Shutting down Werewolf Game API...")


app = FastAPI(
    title="Werewolf Game API",
    description="Realtime Werewolf Game Backend with Auto Host MVP",
    version="0.2.0",
    lifespan=lifespan,
)

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rooms.router)
app.include_router(roles.router)
app.include_router(game.router)
app.include_router(ws.router)


@app.get("/")
async def root():
    return {"message": "🐺 Werewolf Game API", "status": "running", "version": "0.2.0", "docs": "/docs"}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "werewolf-game-backend"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
