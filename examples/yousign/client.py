#!/usr/bin/env python3

import requests
import json
import requests.exceptions
import base64

API_BASE_PRODUCTION = 'https://api.yousign.com'
API_BASE_STAGING = 'https://staging-api.yousign.com'

SIGNATURE_BASE_PRODUCTION = 'https://app.yousign.com/procedure/sign?members='
SIGNATURE_BASE_STAGING = 'https://staging-app.yousign.com/procedure/sign?members='

class Client(object):

    api_key = None
    mode = None
    debug = False
    headers = {}

    def __init__(self, api_key, production=False, debug=False):

        self.headers['Authorization'] = 'Bearer {0}'.format(api_key)

        self.api_key = api_key
        self.api_base = API_BASE_PRODUCTION if production else API_BASE_STAGING
        self.debug = debug
        self.signature_base = SIGNATURE_BASE_PRODUCTION if production else SIGNATURE_BASE_STAGING

    def _create_procedure(self, procedure):
        return self._request(
            '/procedures', method='POST', data=procedure)

    def list_procedures(self):
        return self._request('/procedures')

    def _create_file(self, file, procedure):
        payload = file
        payload['procedure'] = procedure
        return self._request('/files', method='POST', data=payload)

    def _create_member(self, member, procedure):

        payload = member
        payload['procedure'] = procedure

        return self._request('/members', method='POST', data=payload)

    def _create_file_object(self, file_object, procedure, document, member):

        payload = file_object
        payload['procedure'] = procedure
        payload['file'] = document
        payload['member'] = member

        return self._request('/file_objects', method='POST', data=payload)

    def _start_procedure(self, procedure):

        payload = {
            "start": True
        }

        return self._request(procedure, method='PUT', data=payload)

    def _get_signature_link(self, member_id):
        url = self.signature_base + member_id
        return url

    def _request(self, endpoint, method='GET', params=dict(), data=None, files=None):

        url = self.api_base + endpoint

        try:

            if method in ['GET', 'DELETE']:
                response = requests.request(
                    method, url, headers=self.headers, params=params)

            elif method in ['POST', 'PUT']:
                response = requests.request(
                    method, url, headers=self.headers, params=params, json=data)

            response = json.loads(response.text)
            
            if self.debug :
                print(response)

        except requests.exceptions.HTTPError as errh:
            print('Http Error:', errh)
        except requests.exceptions.ConnectionError as errc:
            print('Error Connecting:', errc)
        except requests.exceptions.Timeout as errt:
            print('Timeout Error:', errt)
        except requests.exceptions.RequestException as err:
            print('OOps: Something Else', err)

        return response
