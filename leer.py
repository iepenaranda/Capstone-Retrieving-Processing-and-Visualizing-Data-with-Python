import csv
import sqlite3
from datetime import datetime
import checkDB

#https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv

# Crea la BD donde se guardaran los datosen caso de que no exista.
con = sqlite3.connect('covid.sqlite')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS dias
    (id INTEGER PRIMARY KEY AUTOINCREMENT, iso_code TEXT, continent TEXT, 
    location TEXT, fecha TEXT, total_cases INTEGER, new_cases INTEGER, 
    total_deaths INTEGER, new_deaths INTEGER, total_tests INTEGER, new_tests INTEGER,
    UNIQUE(location, fecha))''')

# Lee el archivo .csv que hay en la carpeta Data y extrae los datos según sea solicitado
# Solicita el país del cuál se desea la información, por lo tanto es necesario escribirlo bien.
with open('Data\owid-covid-data.csv', newline='') as csvfile:
    while True:
        lector = csv.reader(csvfile, delimiter=',')
        print('Enter the name of the country that you want to get data: ')
        location = input()
        print('Searching data of: '+location)
        try:
            last_date = checkDB.lastDate(cur,location)
            if last_date is None:
                desdeCero = True
            else:
                desdeCero = False
            for row in lector:
                if row[2] == location:
                    if desdeCero:
                        if not row[4]:
                            row[4] = 0
                        if not row[5]:
                            row[5] = 0
                        if not row[7]:
                            row[7] = 0
                        if not row[8]:
                            row[8] = 0
                        if not row[25]:
                            row[25] = 0
                        if not row[26]:
                            row[26] = 0
                        
                        cur.execute('''INSERT OR IGNORE INTO dias (iso_code, continent, location, fecha, 
                        total_cases, new_cases, total_deaths, new_deaths, new_tests, total_tests) VALUES (?,?,?,?,?,?,?,?,?,?)''',
                        (row[0],row[1],row[2],row[3],row[4],row[5],row[7],row[8],row[25],row[26]))
                        con.commit()
                    else:
                        if row[3] == last_date:
                            print("Date uploaded")
                            desdeCero = True
                        else:
                            pass
                else:
                    pass
        except KeyboardInterrupt:
            print('')
            print('Program interrupted by user...')
            cur.close()
            break
cur.close()

                
