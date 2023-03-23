from prediction import Prediction
from NextWordPred_db import Predictor_Database
from flask import Flask, request, render_template
from flask_cors import CORS
from flask_restful import reqparse
import pandas as pd
import pyttsx3
import speech_recognition as sr
import webbrowser as wb
import speakEngine

chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
# Speech recognizer


# https://pyttsx3.readthedocs.io/en/latest/engine.html
# TODO
# Speak instructions to user
# Speech to text and read out the 3 words reccomended or type out the first word


app = Flask(__name__)
cors = CORS(app)

prediction = Prediction()
pred_db = Predictor_Database('WORD_RECORD')

data_put_args = reqparse.RequestParser()
data_put_args.add_argument("word", type=str, help="Word Typed")
data_put_args.add_argument("isPredict", type=str,
                           help="Is Word Prrdicted (Y/N)")
data_get_args = reqparse.RequestParser()
data_get_args.add_argument("data", type=str, help="Word Typed")

# Render Application landing page


@app.route("/")
def index():
    #textToSpeech("Enter username and password")
    return render_template('login.html')


@app.route('/main', methods=['POST'])
def main():
    print("reached main")
    uname = request.form['uname']
    passwrd = request.form['pass']
    if uname == "viviana" and passwrd == "123456":
        print("password matched")
        # textToSpeech(uname)
        #textToSpeech("Welcome to Next word prediction application")
        return render_template('main.html', name=uname)


@app.route('/collectFeedback')
def collectFeedback():
    print("collectFeedback")
    textToSpeech("Please answer some of the questions")
    return render_template('feedback_form.html')


@app.route('/back')
def back():
    print("backmethod")
    return render_template('login.html')


@app.route('/signUp')
def signUp():
    print("Entered signUp")
    textToSpeech("Not a memebr. You need to create account")
    return render_template('signup.html')


@app.route('/GoodBye', methods=['POST'])
def home():
    print("GoodBye")
    textToSpeech("Your feedback has been noted")
    return render_template('ThankYou.html')


# API call to get user's speech
@app.get("/speech")
def getSpeech():
    wordSaid = speechToText()
    return {
        "wordSaid": wordSaid,
    }


# API call to obtain next pridected word
@app.get("/prediction")
def get_next_words():
    data = request.args['data']
    predict_word = prediction.get_words_prediction(data)
    wordsToRead = getPredictions(predict_word)
    # Checks to see if there are words to be predicted
    if len(wordsToRead) == 0:
        textToSpeech(
            "Cannot Predict Word, Please keep typing and I will provide help.")
    else:
<<<<<<< .merge_file_gjsgtl

=======
>>>>>>> .merge_file_dPYeU6
        textToSpeech("Your next predicted words are")
        for word in wordsToRead:
            textToSpeech(word)
    return predict_word


# API call to fetch data from Excel to be displayed on Web Application
@app.get("/excelData")
def get_excelData():
    data = pred_db.readAll()
    # print(data)
    return data


# API call to update Word into Excel
@app.put("/excelData")
def put_excelData():
    args = data_put_args.parse_args()
    word = args['word'].lower()
    print("Entered word :", word)
    isPredict = args['isPredict']
    word = format_word(word)
    print("Formatted word : '"+word+"'")
    data = pred_db.readAll()
    pred_db.updInsertDb(dict(key='WORD', value=word), dict(
        WORD=word, COUNT=1, FLAG=isPredict), isPredict)
    return data


# Function to convert speech to text
def speechToText():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening for audio...')
        audio = r.listen(source)
        print('Done!')
    try:
        text = r.recognize_google(audio)
        print('You said:\n' + text)
        return text

    except Exception as e:
        print(e)


# Function to run text to speech
def textToSpeech(word):
    engine = None
    engine = pyttsx3.init()
    engine.say(word)
    engine.runAndWait()
    # engine.iterate


# Function to adjust TTS volume
def changeVolume(change):
    engine = pyttsx3.init()
    volume = engine.getProperty('volume')
    if (change == 'up'):
        volume += 0.05
    else:
        volume -= 0.05
    engine.setProperty('volume', volume)

# Function get three words from payload


def getPredictions(data):
    wordsToPredict = []
    for entries in data:
        if (entries["accuracy"] != 0):
            wordsToPredict.append(entries["name"])
    return wordsToPredict


# Filter word to allow only alphanumeric character and '-' character
def format_word(word):
    if not word.isalnum():
        sample_list = []
        for i in word:
            if i.isalnum() or i == '-':
                sample_list.append(i)
        word = "".join(sample_list)
    return word.strip()

# Append new row to Excel


def append_row(df, row):
    return pd.concat([df, pd.DataFrame([row], columns=row.index)]).reset_index(drop=True)


if __name__ == "__main__":
    app.run()
