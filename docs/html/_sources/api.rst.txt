API
===

Basic Usage
-----------

.. code-block:: python3

  from alexa import Alexa, statement

  app = Alexa('My App Name')

  @app.intent('SayJoke')
  def say_joke():
      return statement('Sorry, I am not feeling funny today.')

  handle_lambda_event = app.handle_lambda_event

The Application Global
----------------------

If you're coming from Flask, you'll be familiar with an application global
``g``, which you can use to assign application-level variables like a database
connection to. PyAlexaLambda has the same idea:

.. code-block:: python3

  from alexa import Alexa, statement, g

  def on_launch():
      g.database = connect_to_database()

  app = Alexa('My App Name')
  app.launch(on_launch)

  @app.intent('Stuff')
  def stuff():
      # do something with g.database
  handle_lambda_event = app.handle_lambda_event

Module Documentation
--------------------

.. automodule:: alexa
  :members:
