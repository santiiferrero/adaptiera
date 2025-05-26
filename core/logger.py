import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from .config import settings

def setup_logger():
    """Configura el sistema de logging de la aplicación."""
    logger = logging.getLogger("ia_adaptiera")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para archivo
    log_file = Path(settings.LOG_FILE)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = setup_logger() 