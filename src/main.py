import os
import sys
import logging
from processor import LogProcessor

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def main():
    log_file = os.getenv('LOG_FILE_PATH', '/data/data.csv')

    if not os.path.exists(log_file):
        logger.error(f"File {log_file} not found.")
        sys.exit(1)

    logger.info(f"Starting analysis for: {log_file}")

    try:
        processor = LogProcessor(log_file)
        processor.run()
        logger.info("Analysis completed successfully.")
    except Exception as e:
        logger.critical(f"System failure: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()