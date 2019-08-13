# -*- coding: utf-8 -*-

import json
import dialogflow_v2 as df


#detect_intent_texts('newagent-855b9', 'arrsrrssd', input(), 'ko-KR')
class NaturalLanguage():
    def __init__(self, project_id, session_id, text, language_code):
        session_client = df.SessionsClient()
        session = session_client.session_path(project_id, session_id)
        text_input = df.types.TextInput(
            text=text, language_code=language_code)
        query_input = df.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        parameter_dict = {}

        for key in response.query_result.parameters:
            key2_data = {}
            if isinstance(response.query_result.parameters[key.encode()], dict) is False:
                parameter_dict['{}'.format(key)] = '{}'.format(response.query_result.parameters[key.encode()])
                print('parameter_dict['+'{}'.format(key)+']{} = '.format(response.query_result.parameters[key.encode()]))
            else:
                for key2 in response.query_result.parameters[key.encode()]:
                    if len('{}'.format(key2)) > 1:
                        key2_data['{}'.format(key2)] = response.query_result.parameters[key.encode()][key2.encode()]
                if len(key2_data.keys()) > 0:
                    if len(key2_data.keys()) == 1:
                        for k, v in key2_data.items():
                            value = v
                    else:
                        value = key2_data
                else:
                    value = '{}'.format(response.query_result.parameters[key.encode()])
                if value != '':
                    parameter_dict['{}'.format(key)] = value

        self.dic = {
                'parameters': parameter_dict,
                'query_text': '{}'.format(response.query_result.query_text),
                'display_name': '{}'.format(response.query_result.intent.display_name),
                'confidence': float('{}'.format(response.query_result.intent_detection_confidence)),
                'fulfillment_text': '{}'.format(response.query_result.fulfillment_text)
        }

    def getParameter(self):
        return self.dic['parameters']

    def getData(self):
        data = self.dic['fulfillment_text'].split(']')[0][1:]
        data = data.split('-')
        for i in [0,1,3]:
            data[i] = int(data[i])
        return data

    def getText(self):
        return self.dic['fulfillment_text'].split('] ')[1]

