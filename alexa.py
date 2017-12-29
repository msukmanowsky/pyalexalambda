import datetime as dt
import logging
import re
from functools import wraps
from typing import Callable, Union
from threading import local


g = local()
log = logging.getLogger('alexa')


def statement(s: str, reprompt: str = None, card_title: str = None, should_end_session: bool = True) -> dict:
    '''Return a plain-text statement.

    :param s: the statement itself
    :param reprompt: text for Alexa to issue if response was not understood
    :param card_title: card title for Echo devices with screens
    :param should_end_session: whether to end the current session or not
    '''
    response = {
        'outputSpeech': {
            'type': 'PlainText',
            'text': s
        },
        'shouldEndSession': should_end_session
    }
    if card_title:
        response['card'] = {
            'type': 'Simple',
            'title': card_title,
            'content': s
        }
    if reprompt:
        response['reprompt'] = {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt
            }
        }

    return response


def question(q: str, reprompt: str = None) -> dict:
    '''Return a plain-text question.

    :param q: the question
    :param reprompt: the plain-text for Alexa to issue if response was not
        understood
    '''
    response = {
        'outputSpeech': {
            'type': 'PlainText',
            'text': q,
        },
        'should_end_session': False
    }
    if reprompt:
        response['reprompt'] = {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt,
            }
        }
    return response


class Alexa:
    '''The main application interface.'''

    def __init__(self, name: str):
        self.name = name
        self._launch_func = None
        self._session_ended_func = None
        self._intent_view_funcs = {}

    def launch(self, func: Callable[[], None]) -> None:
        '''Register (or overwrite) a function to be called when the Lambda
        is launched.

        :param func: the function to call when a LaunchRequest event is
            received.'''
        self._launch_func = func

    def session_ended(self, func: Callable[[], None]) -> None:
        '''Register (or overwrite) a function to be called when the session
        is ended.

        :param func: the function to call when a SessionEndedRequest event is
            received.'''
        self._session_ended_func = func

    def intent(self, name: str):
        '''Decorator used to register the response to an intent.

        :param name: the name of the intent (should match what is in the alexa
            console).'''
        def decorator(f):
            self._intent_view_funcs[name] = f
            @wraps(f)
            def wrapper(*args, **kwargs):
                return f(*args, **kwargs)
            return wrapper
        return decorator

    def build_response(self, response: Union[str, dict]):
        global g

        if response is None:
            return None

        if isinstance(response, str):
            response = statement(response)

        return {
            'version': '1.0',
            'sessionAttirbutes': g.session.get('attributes', {}),
            'response': response,
        }

    def handle_lambda_event(self, event: dict, ctx: dict):
        '''Main entry point / handler for an AWS Lambda.

        :param event: the event payload
        :param ctx: the Lambda context'''
        global g
        assert isinstance(event, dict)
        g.session = event['session']
        g.request = event['request']
        g.context = ctx

        rtype = g.request.get('type')
        intent = g.request.get('intent', {})
        intent_name = intent.get('name', '')

        log.info(f'Received {rtype!r} request.')

        response = None
        if rtype == 'LaunchRequest' and self._launch_func:
            response = self._launch_func()
        elif rtype == 'IntentRequest':
            if intent_name not in self._intent_view_funcs:
                raise ValueError(f'No handler for {intent_name!r} intent.')

            kwargs = {k: v.get('value') for k, v in intent.get('slots', {}).items()}
            response = self._intent_view_funcs[intent_name](**kwargs)
        elif rtype == 'SessionEndedRequest' and self._session_ended_func:
            response = self._session_ended_func(request)

        return self.build_response(response)
