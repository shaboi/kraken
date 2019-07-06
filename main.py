import datetime as dt
import pyodbc, re

from kraken.outlook import *
from kraken.utils import *
from pprint import pprint

# create auth session
auth_outlook()
msgs = fetch_messages('07', '05', '2019')

with open(PATH, 'a+') as writer:
    for msg in msgs:
        line = format_query(list(msg.keys()), list(msg.values()))
        writer.write(str(line) + '\r\n')


'''
# create SQL driver objects
conn = pyodbc.connect('Driver={SQL Server};',
                      'Server=;',  # SERVER
                      'Database= ;',  # DB
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

# most recent date_time stamp in the SQL table
cursor.execute(latest_record_dt)
time_filter = cursor.fetchall()

# filter/exlcude parsed messages with timestamps that come
# before the most recent record; that is, avoid duplicates
for msg in msgs:

    date_time = re.sub(r'[/ ]', ':', str(msg['DATE_TIME']).strip())
    date_time = dt.datetime(date_time.split(':'))

    tail_date_time = re.sub(r'[/ ]', ':', str(time_filter).strip())
    tail_date_time = dt.datetime(tail_date_time.split(':'))

    if date_time < tail_date_time:
        msgs.remove(msg)


for msg in msgs:

    query = format_query(list(msg.keys()), list(msg.values()))

    cursor.execute(query)
    conn.commit()

cursor.close()
conn.close()
'''
