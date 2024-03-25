from datetime import datetime, timezone

def unix_utc_to_datetime(unix_timestamp):
    return datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)