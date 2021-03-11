import sqlite3
import urllib.request

def lastDate(cur,location):
    try:
        last_date = cur.execute('SELECT date FROM dias WHERE location=? ORDER BY date DESC',
        (location,)).fetchone()
        if last_date is None:
            return None
        else:
            return last_date[0]
    except Error:
        return Error