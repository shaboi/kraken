from typing import List


def format_query(cols: List[str], values: List[str]):
    cols, values = str(tuple(cols)), str(tuple(values))
    return f'INSERT INTO Trading.crypto.GO_KRAKEN_SETTLEMENTS {cols} VALUES {values}'


latest_record_dt = 'SELECT DATE_TIME FROM Trading.crypto.GO_KRAKEN_SETTLEMENTS ORDER BY DATE_TIME DESC LIMIT 1'
