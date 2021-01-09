import csv
import sqlite3
from datetime import datetime

con = sqlite3.connect('covid.sqlite')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS dias
    (id INTEGER PRIMARY KEY AUTOINCREMENT, iso_code TEXT, continent TEXT, 
    location TEXT, fecha TEXT, total_cases INTEGER, new_cases INTEGER, 
    total_deaths INTEGER, new_deaths INTEGER, total_tests INTEGER, new_tests INTEGER)''')

with open('data\owid-covid-data.csv', newline='') as csvfile:
    i = 0
    lector = csv.reader(csvfile, delimiter=';')
    for row in lector:
        if i == 0:
            i += 1
            pass
        else:
            if row[2] == 'Colombia':
                #fecha = row[3]
                #date_time_obj = datetime.strptime(fecha, '%d/%m/%Y')
                #dia = date_time_obj.day
                #mes = date_time_obj.month
                #año = date_time_obj.year

                if row[4] == "":
                    row[4] = 0
                if row[5] == "":
                    row[5] = 0
                if row[7] == "":
                    row[7] = 0
                if not row[8]:
                    row[8] = 0
                if row[25] == "":
                    row[25] = 0
                if row[26] is "":
                    row[26] = 0
                cur.execute('''INSERT OR IGNORE INTO dias (iso_code, continent, location,
                fecha, total_cases, new_cases, total_deaths, new_deaths, new_tests, total_tests) VALUES (?,?,?,?,?,?,?,?,?,?)''',
                (row[0],row[1],row[2],row[3],row[4],row[5],row[7],row[8],row[25],row[26]))
                con.commit()
                i += 1
                print(i)
            else:
                pass            
    cur.close()