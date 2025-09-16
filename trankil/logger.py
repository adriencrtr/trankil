from pathlib import Path

from loguru import logger

__all__ = ["logger"]

log_path = Path("logs/app.log")
log_path.parent.mkdir(parents=True, exist_ok=True)

logger.add(
    log_path,
    rotation="500 KB",
    retention="7 days",
    level="DEBUG",
    encoding="utf-8",
    backtrace=True,
    diagnose=True,
)
