import random
from tkinter import *

import pandas

BACKGROUND_COLOR = "#B1DDC6"
FONT1 = ("Ariel", 35, "italic")
FONT2 = ("Ariel", 60, "bold")

try:
    wordlist = pandas.read_csv("./data/unknown.csv")
except FileNotFoundError:
    wordlist = pandas.read_csv("./data/french_words.csv")
    wordlist = wordlist.to_dict(orient='records')
else:
    wordlist = wordlist.to_dict(orient='records')

current_w = {}


def flip_card():
    canvas.itemconfig(canvas_img, image=back)
    canvas.itemconfig(lang, text="English", fill="white")
    canvas.itemconfig(word, text=current_w["English"], fill="white")


def new_card():
    global current_w, flip_timer
    window.after_cancel(flip_timer)
    current_w = random.choice(wordlist)
    canvas.itemconfig(canvas_img, image=front)
    canvas.itemconfig(lang, text="French", fill="black")
    canvas.itemconfig(word, text=current_w["French"], fill="black")
    flip_timer = window.after(3000, flip_card)


def is_known():
    wordlist.remove(current_w)
    new_card()
    data = pandas.DataFrame(wordlist)
    data.to_csv("data/unknown.csv", index=False)


window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526, highlightthickness=0)
front = PhotoImage(file="./images/card_front.png")
back = PhotoImage(file="./images/card_back.png")
wrong_img = PhotoImage(file="./images/wrong.png")
right_img = PhotoImage(file="./images/right.png")
canvas_img = canvas.create_image(400, 263, image=front)
lang = canvas.create_text(400, 100, fill="black", font=FONT1)
word = canvas.create_text(400, 263, fill="black", font=FONT2)
canvas.grid(column=0, row=0, columnspan=2)

wrong = Button(image=wrong_img, highlightthickness=0, command=new_card)
wrong.grid(column=0, row=1)

right = Button(image=right_img, highlightthickness=0, command=is_known)
right.grid(column=1, row=1)

new_card()

window.mainloop()
