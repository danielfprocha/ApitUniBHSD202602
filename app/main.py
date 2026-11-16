from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import registros
from app.core.database import criar_tabelas


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()
    yield


app = FastAPI(
    title="API de Gerenciamento - Projeto A3",
    description="Template inicial integrando FastAPI, SQLite e validações Pydantic.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(registros.router)