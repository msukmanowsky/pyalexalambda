.. PyAlexaLambda documentation master file, created by
   sphinx-quickstart on Thu Dec 28 19:58:11 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PyAlexaLambda
=============

.. toctree::
   :maxdepth: 2

   api

A zero-dependency Python module that makes it easy to write AWS Lambda-based
Alexa apps.

Copy and paste ``alexa.py`` into your Python 3.6 Lambda and add an ``app.py``
as so:

.. code-block:: python

  import random

  from alexa import Alexa, g, statement, question

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

The API for this project is heavily inspired by the wonderful
`Flask-Ask <https://github.com/johnwheeler/flask-ask>`_ package/Flask extension.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
