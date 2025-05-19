import csv
import random


def get_songs():
    # retrieve songs from csv file and put them in a list
    file = open("Song Lyric Spreadsheet - Sheet1.csv", "r")
    all_songs = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_songs.pop(0)

    return all_songs


all_song_list = get_songs()
random_song = random.choice(all_song_list)

song = random_song[0]
lyric = random_song[1]
correct_answer = random_song[2]
wrong_answer_1 = random_song[3]
wrong_answer_2 = random_song[4]
wrong_answer_3 = random_song[5]

answer_list = [correct_answer, wrong_answer_1, wrong_answer_2, wrong_answer_3]
random.shuffle(answer_list)

print(song)
print(lyric)
print(answer_list)
