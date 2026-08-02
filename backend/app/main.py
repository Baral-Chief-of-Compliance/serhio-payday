from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import Settings
from .db import get_session
from .models import PaydayState, Tick

settings = Settings()

app = FastAPI(title="serhio-payday backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/ticks", response_model=list[Tick])
async def get_latest_ticks(session: AsyncSession = Depends(get_session)) -> list[Tick]:
    statement = select(Tick).order_by(Tick.id.desc()).limit(20)
    result = await session.exec(statement)
    return list(result.all())


@app.get("/balance", response_model=PaydayState)
async def get_balance(session: AsyncSession = Depends(get_session)) -> PaydayState:
    state = await session.get(PaydayState, 1)
    if state is None:
        raise HTTPException(status_code=404, detail="Balance not initialized yet")
    return state
