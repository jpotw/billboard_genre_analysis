import csv
import os

tempfile = "temp.csv"

with open('billboard_data.csv', 'r') as csvfile, open(tempfile, 'w', newline='') as outfile:
    reader = csv.reader(csvfile)
    writer = csv.writer(outfile)
    for row in reader:
        date, rank, title, artist = row
        artist = artist.split('&', 1)[0]
        artist = artist.split('Featuring', 1)[0]
        artist = artist.split('x', 1)[0]
        artist = artist.split('X', 1)[0]
        artist = artist.replace('"', '')
        writer.writerow([date, rank, title, artist])

os.remove('billboard_data.csv')
os.rename(tempfile, 'billboard_data.csv')