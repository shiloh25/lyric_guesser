import time


def countdown(timer_amount):
    while timer_amount:
        minutes, secs = divmod(timer_amount, 60)
        timer = "{:02d}:{:02d}".format(minutes, secs)
        print(timer, end='\r')
        time.sleep(1)
        timer_amount -= 1

    print("Time is up")


timer_amount = input("Enter the time in seconds: ")

countdown(int(timer_amount))
