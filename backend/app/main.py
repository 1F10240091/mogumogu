from fastapi import FastAPI

from . import models  # noqa: F401  (テーブル定義の登録)
from .database import engine
from .routers import recipes

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="MoguMogu API", version="0.1.0")

app.include_router(recipes.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
