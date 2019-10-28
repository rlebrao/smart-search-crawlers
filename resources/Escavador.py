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
        if(not util.checkAuthorization(request.headers)):
            return {"message": "ERROR: Chave de acesso inválida"}, 401
        else:    
            response = requests.request('POST', self.URL, headers=self.HEADERS,
            json=self.PAYLOAD, verify=False)
            if response.status_code:
                response = response.json()
                access_token = response['access_token']
                expires_in = response['expires_in']
                refresh_token = response['refresh_token']
                try:
                    params = request.get_json()
                except Exception as e:
                    return {"message":"Parâmetro inválido"},400
                if params:
                    if 'term' in params:
                        return self.search_paid(access_token, params['term'])
                    elif 'cpf' in params:
                        return self.free_search(access_token, params['cpf'])
                    else:
                        return {"message":"Parâmetro inválido"}, 400
                else:
                    return {"message":"Parâmetros obrigatórios não enviados"}, 400

    def search_paid(self, access_token, search_term):
        url = 'https://www.escavador.com/api/v1/busca'

        params = {
            'q': search_term,  
            'qo': 't',  
            'page': '1'  # opcional
        }

        headers = {
            'Authorization': "Bearer {}".format(access_token),
            'X-Requested-With': 'XMLHttpRequest'
        }

        response = requests.request('GET', url, headers=headers, params=params, verify=False)
        if response.status_code is 200:
            return response.json()['items']
        else:
            return {"message":"Falha na consulta"}, 400

    def free_search(self, access_token, cpf):
        url = 'https://www.escavador.com/api/v1/async/resultados'
        headers = {
            'Authorization': 'Bearer {}'.format(access_token),
            'X-Requested-With': 'XMLHttpRequest'
        }
        url = url + "?BUSCA_POR_DOCUMENTO={}".format(cpf)
        response = requests.request('GET', url, headers=headers, verify=False)
        # print(response)
        json_response = response.json()
        if len(json_response['items']) == 0:
            return {"message":"Dados não encontrados para esse CPF"}, 404
        if response.status_code is 200:
            return json_response
        else:
            return {"message":"Falha na busca"},400