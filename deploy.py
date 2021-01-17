from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words


from fastpunct import FastPunct
fastpunct = FastPunct('en')


from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        self.initUI()

    def button_clicked(self):
        self.label.setText("Recording you!")
        self.update()

        LANGUAGE = "english"
        SENTENCES_COUNT = 5  #collects the x number of relevant sentences.

        import speech_recognition as sr
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

        # obtain audio from the microphone
        r = sr.Recognizer()
        commentary = ""

        while True:
            with sr.Microphone(1) as source:
                print("Say something!")
                audio = r.listen(source)
            # recognize speech using Google Speech Recognition
            try:
                speech = r.recognize_google(audio)
                print("You said " + speech) # use default Google API key `r.recognize_google(audio, key = implied)`
                commentary = commentary + speech # + ". "
                if "Corpus" in speech:
                    commentary = commentary - "corpus"
                    break
            except sr.UnknownValueError:
                print("Speech Recognition didn't catch that")
            except sr.RequestError as e:
                print("Could not request results from Speech Recognition service; {0}".format(e))
            except KeyboardInterrupt:
                break

        print("PRE-PUNCTUATION:", commentary, "\n")
        commentary = (fastpunct.punct([commentary], batch_size=32))
        print("PUNCTUATED", commentary, "\n")

        parser = PlaintextParser.from_string(commentary, Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)

        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        print("SUMMARIZED TEXT:")
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            print(sentence)

    def initUI(self):
        self.setGeometry(500, 500, 300, 300)
        self.setWindowTitle("Voice2Notes")

        self.label = QtWidgets.QLabel(self)
        self.label.setText("Translate speech to summarized text!")
        self.label.move(50,50)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Click me to start recording!")
        self.b1.clicked.connect(self.button_clicked)

    def update(self):
        self.label.adjustSize()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

window()
