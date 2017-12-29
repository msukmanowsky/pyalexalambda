# PyAlexaLambda

A zero-dependency Python module that makes it easy to write AWS Lambda-based
Alexa apps.

Copy and paste `alexa.py` into your Python 3.6 Lambda and add an `app.py` as so:

```python
import random

from Alexa import Alexa, g, statement, question

app = Alexa('My Joke App')
jokes = [
    'What goes up and down but does not move? Stairs',
    'Where should a 500 pound alien go? On a diet.',
    'What did one toilet say to the other? You look a bit flushed.',
]


@app.intent('SayJoke')
def say_joke():
    joke = random.choice(jokes)
    return statement(joke)


@app.intent('Sing99Bottles')
def sing_99_bottles(Times: str = '5'):
    times = int(Times)
    sentences = [f'{i} bottles of beer on the wall, {i} bottles of beer. You take one down, you pass it around, {i-1} bottles of beer on the wall' for i in range(times)]
    return statement('')

handle_lambda_event = app.handle_lambda_event
```

The API for this project is heavily inspired by the wonderful [Flask-Ask](https://github.com/johnwheeler/flask-ask) package/Flask extension.
