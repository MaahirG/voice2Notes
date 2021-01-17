from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile

from fastpunct import FastPunct
fastpunct = FastPunct('en')


LANGUAGE = "english"
SENTENCES_COUNT = 5
commentary = ""

import speech_recognition as sr
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

# obtain audio from the microphone
r = sr.Recognizer()


root = tk.Tk()

canvas = tk.Canvas(root, width=1000, height=500)
canvas.grid(columnspan=3, rowspan=3)

#logo
logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

#instructions
instructions = tk.Label(root, text="Click to start summarizing speech!", font="Raleway")
instructions.grid(columnspan=3, column=0, row=1)

def listen():
    button_text.set("Listening...")
    commentary = ""

    text_box = tk.Text(root, height=10, width=50, padx=15, pady=15)
    text_box.tag_configure("left", justify="left")
    text_box.tag_add("left", 1.0, "end")
    text_box.grid(column=0, row=3)
    
    punctuated_text = tk.Text(root, height=10, width=50, padx=15, pady=15)
    punctuated_text.insert(1.0, "SOON TO BE PUNCTUATED TEXT")
    punctuated_text.tag_configure("left", justify="left")
    punctuated_text.tag_add("left", 1.0, "end")
    punctuated_text.grid(column=1, row=3)

    summarized_text = tk.Text(root, height=10, width=50, padx=15, pady=15)
    summarized_text.insert(1.0, "SOON TO BE SUMMARIZED TEXT")
    summarized_text.tag_configure("left", justify="left")
    summarized_text.tag_add("left", 1.0, "end")
    summarized_text.grid(column=2, row=3)

    while True:
        with sr.Microphone(1) as source:
            print("Say something!")
            audio = r.listen(source)

        try:
            speech = r.recognize_google(audio)
            if "Corpus" in speech:
                break

            print("You said: " + speech)
            commentary = commentary + " " + speech

            text_box.delete(1.0, tk.END)
            text_box.insert(1.0, commentary)

        except sr.UnknownValueError:
            print("Speech Recognition didn't catch that")
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))

    button_text.set("ADDING PUNCTUATION!")

    print("PRE-PUNCTUATION:", commentary, "\n")
    commentary = (fastpunct.punct([commentary], batch_size=32))
    print("PUNCTUATED", commentary, "\n")

    punctuated_text.delete(1.0, tk.END)
    punctuated_text.insert(1.0, commentary)

    button_text.set("SUMMARIZING!")

    parser = PlaintextParser.from_string(commentary, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    print("SUMMARIZED TEXT:")
    fullSummary = []
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)
        fullSummary.append(sentence)

    print(fullSummary)
    # new = ' '.join(fullSummary)
    # print(type(new))
    summarized_text.delete(1.0, tk.END)
    summarized_text.insert(1.0, fullSummary)

    button_text.set("Start Recording")


# Multithread so GUI doesn't hang!
def multi():
    threading.Thread(target=lambda:listen()).start()


import threading

button_text = tk.StringVar()
browse_btn = tk.Button(root, textvariable=button_text, command=lambda:multi(), font="Raleway", bg="#20bebe", fg="white", height=2, width=25
)

button_text.set("Start Recording")
browse_btn.grid(column=1, row=2)

root.mainloop()
