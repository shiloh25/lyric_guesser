import csv
import random
from tkinter import *
from functools import partial


# helper functions go here
def get_songs():
    # retrieve songs from csv file and put them in a list
    file = open("Song Lyric Spreadsheet - Sheet1.csv", "r")
    # format list appropriately
    all_songs = list(csv.reader(file, delimiter=","))
    # close the file
    file.close()

    # remove the first row
    all_songs.pop(0)

    return all_songs


def get_round_song():
    """
    Get information about the song randomly chosen
    :return: song, lyric, correct answer and list of all answers
    """
    # call get_songs() function
    all_song_list = get_songs()
    # randomly choose a song from the list
    random_song = random.choice(all_song_list)

    # get needed information including song name, lyric, correct answer and all incorrect answers
    song = random_song[0]
    lyric = random_song[1]
    correct_answer = random_song[2]
    wrong_answer_1 = random_song[3]
    wrong_answer_2 = random_song[4]
    wrong_answer_3 = random_song[5]

    # put all possible answers into a list to use later when making the buttons
    answer_list = [correct_answer, wrong_answer_1, wrong_answer_2, wrong_answer_3]
    # shuffle the order of the list randomly so the correct answer is not on the same button each time
    random.shuffle(answer_list)

    return song, lyric, correct_answer, answer_list


# classes start here

# class for the welcome and get rounds area
class StartGame:
    """
    Initial Game interface (asks users how many rounds they would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """
        # set up the starting window
        self.start_frame = Frame(padx=10, pady=10, bg="#0C0C0C")
        self.start_frame.grid()

        # strings for labels
        # introduction string
        intro_string = ("Welcome to Lyric Guessing! In each round you will be given a song lyric "
                        "and you need to select the missing lyric. Good Luck!")

        # choose string requesting how many rounds the user wants
        choose_string = "How many rounds do you want to play?"

        # list of labels to be made (text | font | fg)
        start_labels_list = [
            ["Lyric Guessing", ("Arial", "16", "bold"), "#F7EFFB"],
            [intro_string, ("Arial", "12", "bold"), "#F7EFFB"],
            [choose_string, ("Arial", "12", "bold"), "#F7EFFB"]
        ]

        # create labels and add them to the reference list...
        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1], fg=item[2],
                               wraplength=350, justify="left", pady=10, padx=20, bg="#0C0C0C")
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can be changed to an error message if necessary
        self.choose_label = start_label_ref[2]

        # frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame, bg="#0C0C0C")
        self.entry_area_frame.grid(row=3)

        # input space for the number of rounds
        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#7D28A4", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 - 100 rounds
        """
        # get rounds the user has requested from the input box
        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to the home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#0C0C0C")

        # error message in case of invalid input
        error = "Please choose a whole number more than zero and less than 100"

        # checks that amount to be played is greater than zero and less than 100
        try:
            # make string input into int value
            rounds_wanted = int(rounds_wanted)
            # check if rounds wanted is greater than 0 and less than 100
            if 0 < rounds_wanted <= 100:
                has_errors = "no"
                # invoke Play class (and take across number of rounds)
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")
                Play(rounds_wanted)
                # Hide root window (ie: hide rounds choice window)
                root.withdraw()
                self.start_frame.destroy()

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # loop to play when has_errors = yes because the users input is invalid
        if has_errors == "yes":
            # display the error if necessary
            if has_errors == "yes":
                self.choose_label.config(text=error, fg="#F8CECC", font=("Arial", "10", "bold"))
                self.num_rounds_entry.config(bg="#F4CCCC")
                self.num_rounds_entry.delete(0, END)


# class for playing the game
class Play:
    """
    Interface for playing the Lyric Guessing Game
    """

    def __init__(self, how_many):

        # set rounds played to 0 to start with
        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        # set rounds wanted to the number of rounds the user inputted
        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        self.rounds_won = IntVar()

        # score list
        self.all_scores_list = []

        self.play_box = Toplevel()

        # set up game frame
        self.game_frame = Frame(self.play_box, bg="#0C0C0C")
        self.game_frame.grid(pady=10, padx=10)

        # declare correct answer text variable inside __init__ to avoid errors
        self.correct_answer_text = None

        # body font for most labels
        body_font = ("Arial", "12")

        # list for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), "#0C0C0C", 0],
            ["", ("Arial", "14", "bold"), "#0C0C0C", 1],
            ["", body_font, "#0C0C0C", 2],
            ["", body_font, "#0C0C0C", 4]
        ]

        # formatting the labels
        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1], bg=item[2],
                                    wraplength=300, justify="left", fg="#F7EFFB")
            self.make_label.grid(row=item[3], padx=10, pady=10)

            play_labels_ref.append(self.make_label)

        # retrieve labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.song_title_label = play_labels_ref[1]
        self.lyric_label = play_labels_ref[2]
        self.results_label = play_labels_ref[3]

        # set up lyric buttons
        self.lyric_frame = Frame(self.game_frame, bg="#0C0C0C")
        self.lyric_frame.grid(row=3)

        self.lyric_button_ref = []
        self.lyric_button_list = []

        # create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.lyric_button = Button(self.lyric_frame, font=("Arial", "12"), text="Lyric", fg="#F7EFFD",
                                       width=15, command=partial(self.round_results, item), bg="#7D28A4")
            self.lyric_button.grid(row=item // 2, column=item % 2, pady=5, padx=5)

            self.lyric_button_ref.append(self.lyric_button)

        # frame to hold hints and stats button
        self.hints_stats_frame = Frame(self.game_frame, bg="#0C0C0C")
        self.hints_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | column
        control_button_list = [
            [self.game_frame, "Next Round", "#7D28A4", self.new_round, 21, 5, None],
            [self.hints_stats_frame, "Hints", "#CBA9DB", self.to_hints, 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#CBA9DB", self.to_stats, 10, 0, 1],
            [self.game_frame, "End", "#7D28A4", self.close_play, 21, 7, None],
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2], command=item[3],
                                         font=("Arial", "16", "bold"), fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.to_help_button = control_ref_list[1]
        self.to_stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # disable stats button for the start of the game
        self.to_stats_button.config(state=DISABLED)

        # once interface has been created, invoke new round function for first round
        self.new_round()

    # new round function
    def new_round(self):
        """
        Starts a new round with a fresh question and answers.
        """
        # count how many rounds have been played
        rounds_played = self.rounds_played.get() + 1
        self.rounds_played.set(rounds_played)
        rounds_wanted = self.rounds_wanted.get()

        # Get the correct song, lyric, correct answer, and shuffled options
        song, lyric, correct_answer, answer_options = get_round_song()
        self.correct_answer_text = correct_answer

        # Update GUI text
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.song_title_label.config(text=f"{song}", fg="#F7EFFD")
        self.lyric_label.config(text=lyric)
        self.results_label.config(text="=" * 7, bg="#0C0C0C", fg="#F7EFFD")

        # Assign answers to the buttons
        for i in range(4):
            self.lyric_button_ref[i].config(text=answer_options[i], state=NORMAL)

        # disable the next button
        self.next_button.config(state=DISABLED)

    # round results function
    def round_results(self, user_choice):

        # enable stats button
        self.to_stats_button.config(state=NORMAL)
        # get user the button that the user selects
        selected_answer = self.lyric_button_ref[user_choice].cget('text')

        # check if answer is correct
        if selected_answer == self.correct_answer_text:
            # set message for the correct answer
            result_text = f"Success! '{selected_answer}' is correct"
            result_fg = "#82B366"
            # change to total_score += 1
            self.all_scores_list.append(1)
            self.rounds_won.set(self.rounds_won.get() + 1)
        else:
            # set message for incorrect answer
            result_text = f"Oops! '{selected_answer}' is wrong"
            result_fg = "#F8CECC"
            # change to total_score is nothing
            self.all_scores_list.append(0)

        # show result message to the user
        self.results_label.config(text=result_text, fg=result_fg)

        # disable lyric buttons when an item has been selected
        for item in self.lyric_button_ref:
            item.config(state=DISABLED)

        # if all the rounds have been played
        if self.rounds_played.get() == self.rounds_wanted.get():
            # present game over message
            self.heading_label.config(text="Game Over")
            # calculate success percentage rate to display
            success_rate = self.rounds_won.get() / self.rounds_played.get() * 100
            self.lyric_label.config(text=f"Success Rate: {success_rate:.0f}%")
            # disable next round button
            self.next_button.config(state=DISABLED, text="Next Round")
            self.to_stats_button.config(bg="#CBA9DB")
            self.end_game_button.config(text="Play Again", bg="#7D28A4")
        else:
            # otherwise enable the next button
            self.next_button.config(state=NORMAL)

    def close_play(self):
        # reshow root (ie: close rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()
        # call start game class
        StartGame()

    def to_hints(self):
        """
        displays hints for playing game
        :return:
        """
        # call hints component
        Hints(self)

    def to_stats(self):
        """
        displays hints for playing game
        """
        # retrieve number of rounds
        # won as a number (rather than the self container)
        rounds_won = self.rounds_won.get()
        stats_bundle = [rounds_won, self.all_scores_list]

        # call stats component
        Stats(self, stats_bundle)


# class for the stats component
class Stats:

    """
    Stats calculations and component
    """

    def __init__(self, partner, all_stats_info):

        # extract information from the master list
        rounds_won = all_stats_info[0]
        user_scores = all_stats_info[1]

        # setup dialogue box
        self.stats_box = Toplevel()

        # disable stats button
        partner.to_stats_button.config(state=DISABLED)

        # if user press cross at top, close stats and 'releases' stats button
        self.stats_box.protocol('WM_DELETE_WINDOW', partial(self.close_stats, partner))

        self.stats_frame = Frame(self.stats_box, width=300, height=200, bg="#F7EFFD")
        self.stats_frame.grid()

        # math to populate stats dialogue
        rounds_played = len(user_scores)

        # write the users score to the stats file
        with open("stats_list.txt", "a") as file:
            file.write(f"\n{sum(user_scores)}")

        # calculate success percentage rate
        success_rate = rounds_won / rounds_played * 100
        # calculate total score by adding all the user scores
        total_score = sum(user_scores)

        # read the stats file and store the past scores
        with open("stats_list.txt", "r") as file:
            past_scores = [int(line.strip()) for line in file.readlines() if line.strip() != '']

        # count the lines in the file to use for average
        with open('stats_list.txt', 'r') as file:
            contents = file.read()
            line_count = contents.count('\n')

        # set the lines to use for the average (to prevent dividing by 0 if the file is empty)
        if line_count > 0:
            lines_for_average = line_count
        else:
            lines_for_average = 1

        # calculate the total of all the past scores for the average
        total_for_average = sum(past_scores)
        # calculate average
        average_score = total_for_average / lines_for_average

        # calculate high score from all the past scores
        high_score = max(past_scores)

        # strings for start labels
        success_string = (f"Success Rate: {rounds_won} / {rounds_played}"
                          f"({success_rate:.0f}%)")
        total_score_string = f"Total Score: {total_score}"

        average_score_string = f"Average Score: {average_score:.0f}\n"

        high_score_string = f"Overall High Score: {high_score}\n"

        # fonts and sizing for headings and text
        heading_font = ("Arial", "16", "bold")
        normal_font = ("Arial", "14")

        # Label list (text | font | 'Sticky')
        all_stats_strings = [
            ["Round Stats", heading_font, ""],
            [success_string, normal_font, "W"],
            [total_score_string, normal_font, "W"],
            ["\nAll Stats", heading_font, ""],
            [average_score_string, normal_font, "W"],
            [high_score_string, normal_font, "W"]
        ]

        # formatting for the stats window
        stats_label_ref_list = []
        for count, item in enumerate(all_stats_strings):
            self.stats_label = Label(self. stats_frame, text=item[0], font=item[1],
                                     anchor="w", justify="left", padx=30, pady=5, bg="#F7EFFD")
            self.stats_label.grid(row=count, sticky=item[2], padx=10)
            stats_label_ref_list.append(self.stats_label)

        self.dismiss_button = Button(self.stats_frame, font=("Arial", "16", "bold"),
                                     text="Dismiss", bg="#7D28A4", fg="#FFFFFF", width=20,
                                     command=partial(self.close_stats, partner))
        self.dismiss_button.grid(row=8, padx=10, pady=10)

    # close the stats window
    def close_stats(self, partner):
        partner.to_stats_button.config(state=NORMAL)
        self.stats_box.destroy()


# class for the hints component
class Hints:

    """
    Hints component
    """
    def __init__(self, partner):

        # setup dialogue box and background colour
        background = "#F7EFFD"
        self.help_box = Toplevel()

        # disable help button
        partner.to_help_button.config(state=DISABLED)

        # if user press cross at top, close help and 'releases' help button
        self.help_box.protocol('WM_DELETE_WINDOW', partial(self.close_help, partner))

        # formatting for the help frame
        self.help_frame = Frame(self.help_box, width=300, height=200)
        self.help_frame.grid()

        self.help_hearing_label = Label(self.help_frame, text="Hints",
                                        font=("Arial", "18", "bold"))
        self.help_hearing_label.grid(row=0)

        # help message
        help_text = "To play the game, you must read the lyric on the screen and try to guess what the missing " \
                    "lyric is from four options. To submit your answer, click the button corresponding to your " \
                    "answer. If you are struggling to select the correct lyric, try thinking about which answers " \
                    "works the best. Even if you don't know the answer, you can take a really good guess based " \
                    "on words that rhyme, words that fit into the sentence best and overall what sounds like it " \
                    "would flow the best in a song."

        self.help_text_label = Label(self.help_frame, text=help_text,
                                     wraplength=350, justify="left", font=("Arial", "12"))
        self.help_text_label.grid(row=1, padx=10)

        self.dismiss_button = Button(self.help_frame, font=("Arial", "12", "bold"),
                                     text="Dismiss", bg="#7D28A4", fg="#FFFFFF", command=partial(self.close_help,
                                                                                                 partner))
        self.dismiss_button.grid(row=2, padx=10, pady=10)

        # List and loop to set the background colour on everything except the buttons
        recolour_list = [self.help_frame, self.help_hearing_label, self.help_text_label]

        for item in recolour_list:
            item.config(bg=background)

    # close the help window
    def close_help(self, partner):
        partner.to_help_button.config(state=NORMAL)
        self.help_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Lyric Guessing")
    StartGame()
    root.mainloop()
