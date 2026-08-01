from fastapi import FastAPI

from . import models  # noqa: F401  (テーブル定義の登録)
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hoiku Recipe API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}
