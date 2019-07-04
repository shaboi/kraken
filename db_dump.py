from typing import List
import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server= ;'  #  SERVER
                      'Database= ;'  #  DB
                      'Trusted_Connection=yes;')

cursor = conn.cursor()


def format_query(cols: List[str], values: List[str]):
    cols, values = str(tuple(cols)), str(tuple(values))
    return f'INSERT INTO Trading.crypto.GO_KRAKEN_SETTLEMENTS {cols} VALUES {values}'

x = [
    {'KRKE_TRD_ID': 'RTRZPG4R', 'KRK_SIDE': 'Buys', 'PRICE': '11,481.33', 'QUANTITY': '15.00', 'BASE': 'XBT', 'CURRENCY': 'USD', 'NOTIONAL': '172,219.95', 'DATE_TIME': '2019/07/04 00:49:35', 'BF_SIDE': 'Sell'},
    {'KRKE_TRD_ID': 'RTRB2ZDQ', 'KRK_SIDE': 'Buys', 'PRICE': '11,142.75', 'QUANTITY': '20.00', 'BASE': 'XBT', 'CURRENCY': 'USD', 'NOTIONAL': '222,855.00', 'DATE_TIME': '2019/07/04 00:50:19', 'BF_SIDE': 'Sell'},
    {'KRKE_TRD_ID': 'RTY9S54P', 'KRK_SIDE': 'Buys', 'PRICE': '0.9905', 'QUANTITY': '100', 'BASE': 'USDT', 'CURRENCY': 'USD', 'NOTIONAL': '99,050.00', 'DATE_TIME': '2019/07/04 00:50:49', 'BF_SIDE': 'Sell'}
    ]

for d in x:
    print(format_query(list(d.keys()), list(d.values())))

    #query = format_query()

    #cursor.execute(query)
    #conn.commit()
