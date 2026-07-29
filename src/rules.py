import pandas as pd


class BaseRule:
    def __init__(self, name):
        self.name = name

    def execute(self, df: pd.DataFrame):
        raise NotImplementedError


class FatalMinutelyRule(BaseRule):
    def __init__(self):
        super().__init__("More than 10 fatal errors per minute")

    def execute(self, df: pd.DataFrame):
        fatal_logs = df[df['severity'].str.lower() == 'error']
        if fatal_logs.empty:
            return []

        counts = fatal_logs.resample('1min', on='date').size()
        alerts = counts[counts > 10]

        return [f"ALERT [{self.name}]: {count} errors at {ts}" for ts, count in alerts.items()]


class BundleHourlyRule(BaseRule):
    def __init__(self):
        super().__init__("More than 10 fatal errors per hour for bundle_id")

    def execute(self, df: pd.DataFrame):
        fatal_logs = df[df['severity'].str.lower() == 'fatal']
        if fatal_logs.empty:
            return []

        grouped = fatal_logs.groupby(['bundle_id', pd.Grouper(key='date', freq='1h')]).size()
        alerts = grouped[grouped > 10]

        return [f"ALERT [{self.name}]: Bundle {idx[0]} had {count} errors at {idx[1]}" for idx, count in alerts.items()]