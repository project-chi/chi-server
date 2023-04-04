import json
import logging.config

from fastapi import FastAPI

from chi_server.engine import engine
from chi_server.models import initialize_database
from chi_server.paths import LOGGING_CONFIG
from chi_server.routers import tasks

app = FastAPI(title="chi.server", version="0.2.2")
logger = logging.getLogger("chi_server.main")
logging.config.dictConfig(json.loads(LOGGING_CONFIG.read_text()))

app.include_router(tasks.router)


@app.on_event("startup")
async def on_startup():
    await initialize_database(engine)
    logger.info("Database initialized.")
