import logging
import sys
import os
from config.settings import Settings

# Initialize settings once globally
settings = Settings()

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a logger that adapts to the current environment.

    Behavior:
      • Local environment: logs to console + file (if ENABLE_FILE_LOGGING=True)
      • Azure / other environments: logs only to console (stdout)
    """

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers if logger is already configured
    if logger.hasHandlers():
        return logger

    # --- Console handler (always enabled) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    try:
        console_handler.stream.reconfigure(encoding="utf-8")
    except Exception:
        pass  # Safe fallback for environments without reconfigure()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # --- File handler (only in local if enabled) ---
    if getattr(settings, "ENABLE_FILE_LOGGING", True) and settings.ENVIRONMENT.lower() == "local":
        os.makedirs("logs", exist_ok=True)
        file_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.info("📜 File logging enabled (local environment).")
    else:
        logger.info(f"☁️ Running in {settings.ENVIRONMENT.upper()} — logging to console only.")

    return logger
