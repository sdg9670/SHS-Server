# -*- coding: utf-8 -*-
import os
import json
import dialogflow_v2 as df
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "dialog.json"
'''
def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = df.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))
    a = ""

    text_input = df.types.TextInput(
        text=text, language_code=language_code)

    query_input = df.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))
    print('ky' + response.query_result.parameters['date-time'.encode()])
    print('ky2' + response.query_result.parameters['AlarmContent'.encode()])
'''
def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = df.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))
    a = ""

    text_input = df.types.TextInput(
        text=text, language_code=language_code)

    query_input = df.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    parameter_dict = {}
    for key in response.query_result.parameters:
        value = '{}'.format(response.query_result.parameters[key.encode()])
        if value != '':
            parameter_dict['{}'.format(key)] = value

    dic = {}
    dic['parameters'] = parameter_dict
    dic['query_text'] = '{}'.format(response.query_result.query_text)
    dic['display_name'] = '{}'.format(response.query_result.intent.display_name)
    dic['confidence'] = float('{}'.format(response.query_result.intent_detection_confidence))
    dic['fulfillment_text'] = '{}'.format(response.query_result.fulfillment_text)
    return dic

while True:
    detect_intent_texts('newagent-855b9', 'arrsrrssd', input(), 'ko-KR')