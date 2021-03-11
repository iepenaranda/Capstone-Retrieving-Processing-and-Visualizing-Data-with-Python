import csv
import sqlite3
import urllib.request
from datetime import datetime
import numpy as np
import pandas as pd
import checkDB

# Crea la BD donde se guardaran los datos en caso de que aún no exista la BD.
print('Verificando la base de datos...')
con = sqlite3.connect('covid.sqlite')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS dias
    (id INTEGER PRIMARY KEY AUTOINCREMENT, iso_code TEXT, continent TEXT, 
    location TEXT, date TEXT, total_cases INTEGER, new_cases INTEGER, 
    total_deaths INTEGER, new_deaths INTEGER, total_tests INTEGER, new_tests INTEGER,
    UNIQUE(location, date))''')

# Lee el archivo .csv que hay en la carpeta Data y extrae los datos según sea solicitado
# Solicita el país del cuál se desea la información, por lo tanto es necesario escribirlo bien.
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
file = pd.read_csv(url,na_values='')
file = file.fillna(0)

while True:
    print('Enter the name of the country that you want to get data: ')
    location = input()
    print('Searching data of: '+location)
    try:
        last_date = checkDB.lastDate(cur,location)
        if last_date is None:
            desdeCero = True
        else:
            desdeCero = False
            
        pais = file[file.loc[:,'location']==location]
        
        for i in range(len(pais)):
            if desdeCero:
                cur.execute('''INSERT OR IGNORE INTO dias (iso_code, continent, location, date, total_cases, 
                new_cases, total_deaths, new_deaths, new_tests, total_tests) VALUES (?,?,?,?,?,?,?,?,?,?)''',
                (pais.iloc[i,:].loc['iso_code'],pais.iloc[i,:].loc['continent'],pais.iloc[i,:].loc['location'],
                                 pais.iloc[i,:].loc['date'],pais.iloc[i,:].loc['total_cases'],pais.iloc[i,:].loc['new_cases'],
                                 pais.iloc[i,:].loc['total_deaths'],pais.iloc[i,:].loc['new_deaths'],
                                 pais.iloc[i,:].loc['new_tests'],pais.iloc[i,:].loc['total_tests']))
                con.commit()
            else:
                # Espera hasta llegar a la fecha más reciente y actualiza la bandera desdeCero
                if pais.iloc[i,:].loc['date'] == last_date:
                    print("Date uploaded")
                    desdeCero = True
                else:
                    pass
    except KeyboardInterrupt:
        print('')
        print('Program interrupted by user...')
        cur.close()
        break
        
cur.close()