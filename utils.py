from typing import List


def format_query(cols: List[str], values: List[str]):
    cols, values = str(tuple(cols)), str(tuple(values))
    return f'INSERT INTO [TABLE] {cols} VALUES {values}'


latest_record_dt = 'SELECT DATE_TIME FROM [TABLE] ORDER BY [COL] DESC LIMIT 1'
