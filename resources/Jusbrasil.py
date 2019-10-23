import requests
from flask_restful import Resource
import re
from bs4 import BeautifulSoup
import json
from flask import jsonify, request
from PIL import Image
import pytesseract
import sys
import os
from pdf2image import convert_from_path
import logging
from common import util

class Jusbrasil(Resource):

    URL_TARGET = 'https://www.jusbrasil.com.br/busca'
    PARAM = '?q='

    def getBsObject(self, url_next_layer):
        print("Requesting URL: " + url_next_layer+'\n')
        # print("\n requesting URL:", url_next_layer)
        res_layer = requests.get(url_next_layer).content
        return BeautifulSoup(res_layer, features="lxml")

    def do_crawler(self, **kargs):
        page_result = self.getBsObject(self.URL_TARGET + self.PARAM + kargs.get('nome'))
        print(page_result.find_all('div',{'class':'DocumentSnippet'}))

    def post(self):
        if(not util.checkAuthorization(request.headers)):
            return {"message": "ERROR: Chave de acesso inválida"}, 401
        else:
            params = request.get_json()
            self.do_crawler(nome=params['nome'])