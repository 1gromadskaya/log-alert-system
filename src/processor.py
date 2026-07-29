import pandas as pd
import logging
from rules import FatalMinutelyRule, BundleHourlyRule

LOG_COLUMNS = [
    'id', 'error_message', 'severity', 'log_location', 'mode', 'model',
    'graphics', 'session_id', 'sdkv', 'test_mode', 'flow_id', 'flow_type',
    'sdk_date', 'publisher_id', 'game_id', 'bundle_id', 'appv', 'language',
    'os', 'adv_id', 'gdpr', 'ccpa', 'country_code', 'date'
]

logger = logging.getLogger(__name__)


class LogProcessor:
    def __init__(self, filepath, chunk_size=100000):
        self.filepath = filepath
        self.chunk_size = chunk_size
        self.rules = [FatalMinutelyRule(), BundleHourlyRule()]
        self.columns = LOG_COLUMNS

    def run(self):
        reader = pd.read_csv(
            self.filepath,
            names=self.columns,
            header=0,
            chunksize=self.chunk_size,
            engine='c',
            low_memory=False
        )

        chunk_idx = 1
        for chunk in reader:
            logger.debug(f"Processing chunk {chunk_idx}")

            chunk['date'] = pd.to_datetime(chunk['date'], unit='s')

            for rule in self.rules:
                alerts = rule.execute(chunk)
                for alert in alerts:
                    logger.warning(alert)

            chunk_idx += 1