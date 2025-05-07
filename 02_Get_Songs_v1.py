import csv
import random

# retrieve songs from csv file and put them in a list
file = open("Song Lyric Spreadsheet - Sheet1.csv", "r")
all_songs = list(csv.reader(file, delimiter=","))
file.close()

# remove the first row
all_songs.pop(0)

random_song = random.choice(all_songs)

print(random_song)




