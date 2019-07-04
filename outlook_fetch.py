import imapclient as imp
import email, re

from datetime import datetime
from pprint import pprint

from kraken.config import *

server = imp.IMAPClient(HOST, ssl=True)
server.login(USERNAME, PASSWORD)
server.select_folder('INBOX', readonly=True)

messages = server.search(['FROM', USERNAME])  # otc-confirm@kraken.com

regex = [
     ('KRKE_TRD_ID', r'(?<=Trade #: )[0-9A-Za-z]+'),
     ('KRK_SIDE', r'(?<=Kraken :)\s*\w+'),
     ('PRICE', r'(?<=Unit Price:)\s*[0-9.,]+'),
     ('QUANTITY', r'(?<=U.A. : )(?:Sells|Buys)(\s*[0-9.]+)'),
     ('BASE', r'(?<=Base Asset:)\s*\w+'),
     ('CURRENCY', r'(?<=Currency:)\s*\w{2,4}'),
     ('NOTIONAL', r'(?<=Proceeds:)\s*[0-9.,]+')
]

tickets, tags = [], ["INTERNALDATE", "BODY", "RFC822"]

for id, data in server.fetch(messages, tags).items():

    data = list(data.values())
    date, content = data[1], data[-1].decode('utf-8')

    payload = {tup[0]: re.findall(tup[1], content, re.I)[0] for tup in regex}

    if isinstance(date, datetime):
        payload['DATE_TIME'] = date.strftime("%Y/%m/%d %H:%M:%S")

    if re.search('sell', str(payload['KRK_SIDE']), re.I):
        payload['BF_SIDE'] = 'Buy'
    else:
        payload['BF_SIDE'] = 'Sell'

    payload = {k: v.strip() for k, v in payload.items()}

    tickets.append(payload)


pprint(tickets)
