from tkinter import *


class StartGame:
    """
    Initial Game interface (asks users how many rounds they would like to play)
    """

    def __init__(self, parent):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(parent, padx=10, pady=10, bg="#0C0C0C")
        self.start_frame.grid()

        # strings for labels
        intro_string = ("Welcome to Lyric Guessing! In each round you will be given a song lyric "
                        "and you need to select the missing lyric. Good Luck!")

        # choose string = "Oops - Please choose a whole number more than zero."
        choose_string = "How many rounds do you want to play"

        # List of labels to be made (text | font | fg)
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

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=10,)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#7D28A4", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to the home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#0C0C0C")

        error = "Oops - Please choose a whole number more than zero"

        # checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if 0 < rounds_wanted <= 100:
                has_errors = "no"
                # invoke Play class (and take across number of rounds)
                self.num_rounds_entry.delete(0, END)
                self.choose_label.config(text="How many rounds do you want to play?")
                print(f"{rounds_wanted} is valid")

            elif rounds_wanted <= 0:
                has_errors = "yes"

            elif rounds_wanted > 100:
                has_errors = "yes"

            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        if has_errors == "yes":
            # display the error if necessary
            if has_errors == "yes":
                self.choose_label.config(text=error, fg="#F8CECC", font=("Arial", "10", "bold"))
                self.num_rounds_entry.config(bg="#F4CCCC")
                self.num_rounds_entry.delete(0, END)
                print(f"{rounds_wanted} is not valid")


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Lyric Game")
    StartGame(root)
    root.mainloop()
