"""Logging configuration for D'PARIS EGSOTIS backend."""
import logging
import sys

from app.core.config import settings


def setup_logging() -> None:
    """Configure root logger based on environment."""
    level = logging.DEBUG if settings.DEBUG else logging.INFO

    log_format = (
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s"
        if settings.DEBUG
        else "%(asctime)s | %(levelname)-8s | %(message)s"
    )

    logging.basicConfig(
        level=level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Silence noisy third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.DEBUG else logging.WARNING
    )

    logger = logging.getLogger("dparis")
    logger.info("Logging initialized — level: %s, env: %s", level, settings.ENVIRONMENT)


def get_logger(name: str) -> logging.Logger:
    """Get a named logger."""
    return logging.getLogger(f"dparis.{name}")
