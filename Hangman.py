#Hangman Game by Kieron Stewart
from tkinter import *
import random

root = Tk()
root.wm_title("Hangman")

my_images = []                                      #pre-load images in list
for i in range(0,11):
    im = "/Users/kieronstewart/Documents/Coding/Python/Hangman/Images/image" + str(i) + ".gif"
    my_images.append(PhotoImage(file = im))
im_number = int(0)
guess = str("")

def word_generator():
    lines = open('/Users/kieronstewart/Documents/Coding/Python/Hangman/words.txt').read().splitlines()
    global word, length, word_list
    word = random.choice(lines)[:-1]                #[:-1] deletes "\" at end of each word, due to .txt conversion
    #print(word)                                     #to help
    text_canvas.delete('1.0', END)
    text_canvas.insert(END, " * "*len(word))
    guesses_canvas.delete('1.0', END)
    guesses_canvas.insert(END, "The word has "+str(len(word))+" letters")

def guess_checker(l):
    if l in guess_list: return TRUE
    else: return FALSE

def validate(thing):                                
    thing = thing[0]                                #validating entry, limiting entry to initial character
    if thing in guess_list:                         #testing if guessed before
        return FALSE
        pass
    for i in range(10):                             #testing if guess is a number. Work around where Entry produces a string
        if thing == str(i):
            return FALSE
            pass
    if thing in "!@£$%^&*()_+-=¡€#¢∞§¶•ªº–≠[];'\/.,`§{}|:?><±":
        return FALSE
        pass

    return TRUE

def game(*args):                                    #*args required where referenced in button and <enter>
    global counter, guess_list, guess, guessed_word
    guessed_word = ""

    while True:                                     #while true loop, so to break if any bad/repeated/numerical entries
        guess = entries.get().lower()
        if guess_list == "":
            guesses_canvas.delete('1.0', END)       #first go clears word length note
        if guess == word:                           #if guessed whole word correctly, win
            guessed_word = guess
            text_canvas.delete('1.0', END)
            text_canvas.insert(END, guessed_word)   
            break
        if validate(guess) == 0 :                   #if bad entry, break 
            entries.delete(0, 'end')
            break
        else: 
            guess = guess[0]                        #else take only the first character of enrty
            guess_list = guess_list + guess
            guesses_canvas.insert(END, guess+" ")   #add to current guesses

            for char in word:                       #printout for current successful guesses
                if guess_checker(char) == TRUE:
                    guessed_word = guessed_word+str(char)
                else:
                    guessed_word = guessed_word+" _ "
            text_canvas.delete('1.0', END)
            text_canvas.insert(END, guessed_word)  

            if guess not in word:                   #for a false guess, add to counter
                counter += 1
    
    entries.delete(0, 'end')                    
    picture = my_images[counter]                    #update hangman picture based on counter
    graphics.itemconfig(game_image,image=picture)  
    win_lose(counter, guessed_word)

def win_lose(c, w):
    if c == 10:                                     #maxed number of tries reached, game over
        guesses_canvas.delete('1.0', END)
        guesses_canvas.insert(END, "Game Over\nTry Again")
        text_canvas.delete('1.0', END)
        text_canvas.insert(END, "The word was '"+word+"'A")
        disable()
    if w == word:                                   #fully correct guessed word
        guesses_canvas.delete('1.0', END)
        guesses_canvas.insert(END, "You Won!\nPlay Again?")
        disable()
    else: pass

def disable():
    guess_button.config(state=DISABLED)
    entries.config(state=DISABLED)
    entries.bind('<Return>', NONE )

def enable():
    guess_button.config(state=NORMAL)
    entries.config(state=NORMAL)
    entries.bind('<Return>', game)
    entries.focus()

def new_game():
    global guess_list, counter
    start_image = my_images[0]
    graphics.itemconfig(game_image,image=start_image)
    enable()
    word_generator()
    guess_list = ""
    counter = 0

leftFrame = Frame(root, width=600, height = 600)   
leftFrame.grid(row=0, column=0, padx=10, pady=2)
rightFrame = Frame(root, width=300, height = 600)
rightFrame.grid(row=0, column=1, padx=10, pady=2)

graphics = Canvas(leftFrame, width=550, height=550)
graphics.grid(row=0, column=0, padx=10, pady=2)
whole_image = my_images[10]
game_image = graphics.create_image(275,275,image=whole_image)   #anchor centre image to centre of canvas, coordinates (275,275)

text_canvas = Text(rightFrame, width = 30, height = 5)
text_canvas.config(font=40)
text_canvas.grid(row=0, column=0, columnspan = 2, padx=10, pady=2)
text_canvas.insert(END, "Click new game to start. Guess one letter at a time")

guesses_canvas = Text(rightFrame, width = 30, height = 5)
guesses_canvas.config(font=30)
guesses_canvas.grid(row=1, column=0, columnspan = 2, padx=10, pady=2)

entry_label = Label(rightFrame, text = "Guess:").grid(row=2, column=0, padx=10, pady=2)
entries = Entry(rightFrame, width = 10, textvariable = guess)
entries.grid(row = 2, column=1, padx=10, pady=2)
entries.config(state=DISABLED)
entries.bind('<Return>', NONE )

clear_space = Label(rightFrame, text = "").grid(row=3, column=0, padx=10, pady=2)
guess_button = Button(rightFrame, text = "Enter", command = game)
guess_button.grid(row=4, column=0, columnspan = 2, padx=10, pady=2)
guess_button.config(state=DISABLED)
new_game = Button(rightFrame, text = "New Game", command = new_game)
new_game.grid(row=5, column=0, columnspan = 2, padx=10, pady=2)

root.mainloop() 