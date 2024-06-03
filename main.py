from loguru import logger
import sys
from app.start import run


def run_server():
    try:
        logger.remove()
        logger.add(sys.stdout,
                   format="<green>{time}</green> <level>{level: <8}</level> <cyan>{name}</cyan> -"
                          " <level>{message}</level>",
                   colorize=True)
        run()
    except Exception:
        logger.exception("Run Failed")


if __name__ == "__main__":
    run_server()
