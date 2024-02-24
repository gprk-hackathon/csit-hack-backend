import json
from logging.config import dictConfig


def configure_logging() -> None:
    with open("config/config.json") as f:
        d = json.load(f)
        dictConfig(d["logger"])
