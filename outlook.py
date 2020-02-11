import imapclient as imp
import datetime as dt
import email, re

from kraken.config import *


def auth_outlook(host=HOST, username=USERNAME, password=PASSWORD):
    global server
    server = imp.IMAPClient(host, ssl=True)
    server.login(username, password)
    server.select_folder('INBOX', readonly=True)


def fetch_messages(month, day, yr):
    '''
    Arguments
    ---------
    month, day, yr :: str or int
        filters out messages that come before the declared date;
        format is mm-dd-yyyy

    Returns
    -------
    tickets :: List[dict]
        List of dictionaries of the pertinent, parsed content from
        the fetched emails
    '''

    tickets, filters = [], ["INTERNALDATE", "BODY", "RFC822"]

    regex = [
         ('TRADE_ID', r'(?<=Trade #: )[0-9A-Za-z]+'),
         ('BUY_SIDE', r'(?<=Buy Side:)\s*\w+'),
         ('PRICE', r'(?<=Unit Price:)\s*[0-9.,]+'),
         ('QUANTITY', r'(?<=[HEADER]: )(?:Sells|Buys)(\s*[0-9.]+)'),
         ('BASE', r'(?<=Base Asset Type:)\s*\w+'),
         ('CURRENCY', r'(?<=Note Type:)\s*\w{2,4}'),
         ('NOTIONAL', r'(?<=Denomination:)\s*[0-9.,]+')
    ]

    since = dt.date(int(yr), int(month), int(day))
    # from SENDER or USERNAME, depending
    messages = server.search(['FROM', USERNAME, 'SINCE', since.strftime("%d-%b-%Y")])

    for id, data in server.fetch(messages, filters).items():

        data = list(data.values())
        date, content = data[1], data[-1].decode('utf-8')

        payload = {tup[0]: re.findall(tup[1], content, re.I)[0] for tup in regex}

        if isinstance(date, dt.datetime):
            payload['DATE_TIME'] = date.strftime("%Y/%m/%d %H:%M:%S")

        if re.search('sell', str(payload['BUY_SIDE']), re.I):
            payload['EXCHANGE'] = 'Buy'
        else:
            payload['EXCHANGE'] = 'Sell'

        payload = {k: v.strip() for k, v in payload.items()}
        tickets.append(payload)

    return tickets
