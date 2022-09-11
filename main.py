from tkinter import *
import math  # Needed to round countdown properly

# ---------------------------- CONSTANTS ------------------------------- #
BEIGE = "#FAEBE0"
BROWN = "#BE8C63"
GREEN = "#B5CDA3"
PINK = "#CA4E79"
PURPLE = "#7A4069"
RED = "#D2001A"
SPRING_GREEN = "#36AE7C"
YELLOW = "#F2D388"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None


# ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    """Reset all checkmarks, timer text, stop the timer, and change title to original"""
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer_label.config(text="Timer")
    checkmarks_label.config(text="")
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #

def start_timer():
    global reps
    reps += 1

    work_seconds = WORK_MIN * 60
    short_break_seconds = SHORT_BREAK_MIN * 60
    long_break_seconds = LONG_BREAK_MIN * 60

    if reps % 8 == 0:  # If it's the 8th rep
        countdown(long_break_seconds)
        timer_label.config(text="Big break!", fg=PURPLE)
    elif reps % 2 == 0:  # If it's the 2nd, 4th, or 6th rep
        countdown(short_break_seconds)
        timer_label.config(text="Mini break!", fg=PINK)
    else:  # If it's the 1st, 3rd, 5th, or 7th rep
        countdown(work_seconds)
        timer_label.config(text="Do work!", fg=RED)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
# Because of our mainloop, we cannot simply make a while loop
def countdown(count):
    """Waits a specific amount of time in millisecond, then calls specified function and lowers the starting count by 1"""
    count_minute = math.floor(count / 60)  # Returns whole numer <= x
    count_seconds = count % 60  # Remaining number of seconds after being divided by 60
    if count_seconds < 10:
        count_seconds = f"0{count_seconds}"  # So it doesn't display 5:0 (Dynamic Typing)

    canvas.itemconfig(timer_text, text=f"{count_minute}:{count_seconds}")
    if count > 0:  # Prevents negative numbers
        global timer
        timer = window.after(1000, countdown, count - 1)  # Subtract 1 second each time
    else:
        start_timer()
        checkmarks = ""
        num_work_sessions = math.floor(reps / 2)  # math.floor grounds down to nearest integer
        for i in range(num_work_sessions):
            checkmarks += "✔"
        checkmarks_label.config(text=checkmarks)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro App")
window.config(padx=100, pady=50, bg=YELLOW)

start_button = Button(text="Start", font=(FONT_NAME, 16, "normal"), bg=GREEN, command=start_timer)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", font=(FONT_NAME, 16, "normal"), bg=GREEN, command=reset_timer)
reset_button.grid(row=2, column=2)

timer_label = Label(text="Timer", font=(FONT_NAME, 35, "bold"), bg=YELLOW, fg=BROWN)
timer_label.grid(row=0, column=1)

checkmarks_label = Label(bg=YELLOW, fg=SPRING_GREEN)  # We want it to start empty then add checkmark each work countdown
checkmarks_label.grid(row=3, column=1)

# Canvas widget allows us to layer things on top of each other
canvas = Canvas(width=200, height=224, bg=YELLOW,
                highlightthickness=0)  # image is 223, but even numbers (224) are easier
# to work with.  Highlightthickness got rid of the canvas border
tomato_img = PhotoImage(file="tomato.png")  # if image is somewhere else, provide absolute or relative path
canvas.create_image(100, 112, image=tomato_img)  # first, x,y coordinate required, half the width and height = center
timer_text = canvas.create_text(100, 130, text="00:00", font=(FONT_NAME, 26, "bold"), fill=BEIGE)  # Center of tomato
canvas.grid(row=1, column=1)



window.mainloop()  # "Event driven" through our mainloop, checking to see if something has happened on screen
