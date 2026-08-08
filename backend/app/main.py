"""FastAPI エントリポイント。"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, SessionLocal, engine
from app.middleware import RateLimitMiddleware
from app.routers import auth, children, feedback, menus, recipe_master, recipes, shopping
from app.services.seed import seed_recipes

settings = get_settings()

Base.metadata.create_all(bind=engine)

# レシピマスタのシード投入（初回起動時のみ追加）
with SessionLocal() as db:
    seed_recipes(db)

app = FastAPI(title=settings.app_name, version=settings.version)

if settings.rate_limit_enabled:
    app.add_middleware(
        RateLimitMiddleware,
        max_requests=settings.rate_limit_max_requests,
        window_seconds=settings.rate_limit_window_seconds,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(children.router, prefix="/api/v1")
app.include_router(menus.router, prefix="/api/v1")
app.include_router(recipes.router, prefix="/api/v1")
app.include_router(recipe_master.router, prefix="/api/v1")
app.include_router(shopping.router, prefix="/api/v1")
app.include_router(feedback.router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
