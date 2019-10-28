import requests
from flask_restful import Resource, request
import re
from bs4 import BeautifulSoup
import json
from common import util
from urllib.parse import urlencode

class BolsaFamilia(Resource):
    SITE_URL = 'http://www.transparencia.gov.br/api-de-dados/bolsa-familia-disponivel-por-cpf-ou-nis'
    
    def getBsObject(self, url_next_layer):
        print("Requesting URL: " + url_next_layer)
        # print("\n requesting URL:", url_next_layer)
        res_layer = requests.get(url_next_layer).content
        return BeautifulSoup(res_layer, features="lxml")
    
    def do_crawler(self, **kargs):
        dict_query  = {}
        dict_query['codigo'] = kargs.get('nis')
        dict_query['anoMesReferencia'] = kargs.get('ano_mes_referencia')
        dict_query['anoMesCompetencia'] = kargs.get('ano_mes_competencia')
    
        result = requests.get(self.SITE_URL + "?" + urlencode(dict_query))
        res_json = result.json()
        json_response = {}
        if result.status_code == 400:
            return {"message":"Nenhum resultado encontrado"}, 404
        for key, value in enumerate(res_json[0]):
            json_response[value] = res_json[0][value]
        return json_response

    def post(self):
        if(not util.checkAuthorization(request.headers)):
            return {"message": "ERROR: Chave de acesso inválida"}, 401
        else:
            params = request.get_json()
            if params:
                if 'nis' not in params:
                    return {"message":"Parametro 'nis' é obrigatório"}, 400
                if 'ano_mes_referencia' not in params:
                    return {"message":"Parametro 'ano_mes_referencia' é obrigatório"}, 400
                if 'ano_mes_competencia' not in params:
                    return {"message":"Parametro 'ano_mes_competencia' é obrigatório"}, 400
                else:
                    result = self.do_crawler(nis=params['nis'], ano_mes_competencia = params['ano_mes_competencia'],
                    ano_mes_referencia = params['ano_mes_referencia'])
                    return result
            else:
                return {"message":"Requisição inválida"}, 400
              
