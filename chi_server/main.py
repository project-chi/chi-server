import json
import logging.config

from fastapi import FastAPI

from chi_server.engine import engine
from chi_server.models import initialize_database
from chi_server.paths import LOGGING_CONFIG

app = FastAPI(title="chi.server", version="0.2.1")
logger = logging.getLogger("chi_server.main")
logging.config.dictConfig(json.loads(LOGGING_CONFIG.read_text()))


@app.on_event("startup")
async def on_startup():
    await initialize_database(engine)
    logger.info("Database initialized.")
