import csv
import json

csvfile = open('C:/Users/gaurav.sikka01/Downloads/salesdataset.csv', 'r')
jsonfile = open('file.json', 'w')

fieldnames = ("Store","Dept","Date","Weekly_Sales","IsHoliday")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')