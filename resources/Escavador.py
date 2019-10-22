import requests
from flask_restful import Resource
import re
from bs4 import BeautifulSoup
import json
from flask import jsonify, request
from common import util

class Escavador(Resource):
    URL = 'https://www.escavador.com/api/v1/request-token'

    PAYLOAD = {
        'username': 'rodrigo.lebrao1@gmail.com',  
        'password': 'Snhsmvgl09@'  
    }

    HEADERS = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }

    def post(self):
        response = requests.request('POST', self.URL, headers=self.HEADERS, json=self.PAYLOAD, verify=False)
        if response.status_code:
            response = response.json()
            access_token = response['access_token']
            expires_in = response['expires_in']
            refresh_token = response['refresh_token']
            print(access_token)
