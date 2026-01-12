from fastapi import FastAPI, APIRouter , Request
from fastapi.responses import JSONResponse, HTMLResponse, RedirectResponse, PlainTextResponse
from contextlib import asynccontextmanager
from database import database
import logging
from router.auth_router import router as user_router
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    await database.connect()
    yield
    # Shutdown code here
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(user_router)


