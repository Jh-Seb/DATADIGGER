import csv
with open('data_cities_properati.csv', 'r', encoding="utf8") as cities_properati:
    cities={}
    for line in csv.reader(cities_properati):
        cities.update({line[0]:line[-1]})
for name,value in cities:
    print(name, value)

