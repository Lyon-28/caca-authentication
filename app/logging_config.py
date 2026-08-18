import logging
import json
import sys
from datetime import datetime, timezone
from app.config import settings

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        if hasattr(record, "extra_data"):
            payload.update(record.extra_data)
        return json.dumps(payload)

def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger("caca")
    root.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))
    root.handlers = [handler]
    return root

logger = setup_logging()