import sqlite3
import time
import zlib

conn = sqlite3.connect('covid.sqlite')
cur = conn.cursor()

cur.execute('SELECT location, date, new_cases, new_deaths FROM dias')
daily = dict()
dates = list()
countries = dict()

for row in cur:
    if row[0] not in countries.keys():
        countries[row[0]] = 1
    else:
        countries[row[0]] += 1
    if row[1] not in dates:
        dates.append(row[1])
    key = (row[0], row[1])
    daily[key] = (row[2])

print('There are '+str(len(countries))+' countries in the database.')

for i in countries.keys():
    print(i+' has registered '+str(countries.get(i))+' days.')
print(len(dates))

fhand = open('gline.js','w')
fhand.write("gline = [ ['Date'")
for country in countries.keys():
    fhand.write(",'"+country+"'")
fhand.write("]")

dates.sort()

for date in dates:
    fhand.write(",\n['"+date+"'")
    for country in countries:
        key = (country,date)
        val = daily.get(key,0)
        fhand.write(","+str(val))
    fhand.write("]")

fhand.write("\n];\n")
fhand.close()

print("Output written to gline.js")
print("Open gline.htm to visualize the data")