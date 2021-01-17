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
fastpunct.punct(["oh i thought you were here", "in theory everyone knows what a comma is", "hey how are you doing", "my name is sheela i am in love with hrithik"], batch_size=32)

LANGUAGE = "english"
SENTENCES_COUNT = 10

import speech_recognition as sr
for index, name in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

# obtain audio from the microphone
r = sr.Recognizer()
commentary = ""
try:
    while True:
        with sr.Microphone(1) as source:
            print("Say something!")
            audio = r.listen(source)
        # recognize speech using Google Speech Recognition
        try:
            speech = r.recognize_google(audio)
            print("You said " + speech) # use default Google API key `r.recognize_google(audio, key = implied)`
            commentary = commentary + speech # + ". "
            if "Corpus" in speech or KeyboardInterrupt:
                break
        except sr.UnknownValueError:
            print("Speech Recognition didn't catch that")
        except sr.RequestError as e:
            print("Could not request results from Speech Recognition service; {0}".format(e))

except KeyboardInterrupt:
    pass

# commentary = (fastpunct.punct(commentary, batch_size=32))

# Speaker recognition?
# MAKE LANGUAGE AGNOSTIC - google translate layer

# url = "https://en.wikipedia.org/wiki/Automatic_summarization"
# parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
# parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))

parser = PlaintextParser.from_string(commentary, Tokenizer(LANGUAGE))
stemmer = Stemmer(LANGUAGE)

summarizer = Summarizer(stemmer)
summarizer.stop_words = get_stop_words(LANGUAGE)

for sentence in summarizer(parser.document, SENTENCES_COUNT):
    print(sentence, "\n")