import sqlite3
import time
import zlib

conn = sqlite3.connect('covid.sqlite')
cur = conn.cursor()

cur.execute('SELECT fecha, total_cases, total_deaths FROM dias')
total = dict()
for filas in cur:
    total[filas[0]] = (filas[1], filas[2])

#print(cases.keys())

dates = list()
for date in total.keys():
    dates.append(date)

cur.execute('SELECT fecha, new_cases, new_deaths FROM dias')
news = dict()
for filas in cur:
    news[filas[0]] = (filas[1], filas[2])

print('Loaded days: ',len(dates))

fhand = open('gline.js','w')
fhand.write("gline = [ ['Date', 'New Cases']")

for i in range(len(dates)):
    fhand.write(",\n['"+dates[i]+"'")
    fhand.write(","+str(news.get(dates[i])[0]))
    fhand.write("]")

fhand.write("\n];\n")
fhand.close()

print("Output written to gline.js")
print("Open gline.htm to visualize the data")