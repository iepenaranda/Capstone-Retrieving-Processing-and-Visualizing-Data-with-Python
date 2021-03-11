import sqlite3
import urllib.request


# Esta función busca la última fecha registrada en la BD y la guarda
# Esto permite después al algoritmo reconocer desde donde empezar a carga la información
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