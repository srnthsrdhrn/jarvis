import logging
import requests

from flask import Flask

from flask_ask import Ask, question, convert_errors, statement, session, request

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def greet():
    return question('Jarvis is Online! What is your name?')


@ask.intent("GreetNormal", default={'simple': ''})
def simple():
    return question('Hi, I am Jarvis, What is your name?')


@ask.intent("Info", default={'namesa': ''})
def info():
    return question('I am Jarvis, Speed 1 tera hertz , Memory 1 zeta Byte')


@ask.intent("AMAZON.YesIntent")
def yes():
    msg = ""
    news1 = session.attributes['news']
    news_feed = news1[0]
    msg += 'Title, ' + news_feed['title']
    msg += ', Description, ' + news_feed['description']
    msg += ', Do you want anything else?'
    return question(msg)


@ask.intent("GetUserName", mapping={'user': 'username'})
def name(user):
    if user in convert_errors:
        return question('Hi There {}'.format(user)+', what would you like me to do?')
    return question('Hi There {}'.format(user)+', what would you like me to do?')


@ask.intent("AMAZON.NoIntent")
def no():
    return question("Ok, What else would you like me to do?")


@ask.intent("AMAZON.CancelIntent")
def cancel():
    return statement('Ok, Jarvis is going offline. bye!')


@ask.intent("AMAZON.StopIntent")
def stop():
    return question('Ok, the action is stopped')


@ask.intent("GetNews")
def news():
    response = requests.get(
        "https://newsapi.org/v1/articles?source=national-geographic&sortBy=top&apiKey=44d2ab2402f3450798f88d16bab96b8e")
    json_response = response.json()
    sources = json_response['source']
    news2 = json_response['articles']
    session.attributes['news'] = news2
    msg = 'There is one news sourced from ' + sources + ', would you like to hear it?'
    return question(msg)


@ask.intent("SpeechIntent")
def speechfunc(speech):
    if speech == 'News' or speech == 'news':
        obj = news()
        return obj
    elif speech == 'jarvis' or speech == 'Jarvis' or speech == 'hi':
        obj = greet()
        return obj
    return question('I misinterpreted what you spoke, Did you say , ' + speech+' ?')


if __name__ == '__main__':
    app.run(debug=True)
