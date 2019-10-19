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

class Sivec(Resource):
    HOSTNAME = 'http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com'
    SITE_NAME = 'sivec'   
    TARGET_URL = "{}/{}/login.html".format(HOSTNAME,SITE_NAME)
    
    dirname = os.path.dirname
    PDF_FILES = os.path.join(dirname(dirname(__file__)), 'pdf-files')
    TXT_FILES = os.path.join(dirname(dirname(__file__)), 'txt-files')

    def getBsObject(self, url_next_layer):
        print("\n requesting URL:", url_next_layer)
        res_layer = requests.get(url_next_layer).content
        return BeautifulSoup(res_layer, features="lxml")

    def get_full_url(self, path):
        if path.find('location.href') > -1:
            path = re.sub("location.href='",'',path)
            path = re.sub("'",'',path)
            path = re.sub(";",'',path)
        elif path.find('window.location') > -1:
            path = re.sub("window.location=",'',path)
            path = re.sub("'",'',path)
            path = re.sub(";",'',path)

        return '{}/{}/{}'.format(self.HOSTNAME, self.SITE_NAME, path)
    
    def getFieldFromTxt(self, _regex, txt_content):
        try:
            return re.search(_regex, str(txt_content)).group()
        except:
            return ""

    def do_crawler(self, nome_completo):
        json_response = {}
        bs_obj = self.getBsObject(self.TARGET_URL)
        page2_url = bs_obj.find('form', id="nomeForm").get('action')
        page2_url = self.get_full_url(page2_url)

        bs_obj2 = self.getBsObject(page2_url)
        url_pesquisa_rg = self.get_full_url(bs_obj2.find("a", text="Por RG").get('href'))
        url_pesquisa_nome = self.get_full_url(bs_obj2.find("a", text="Por Nome").get('href'))
        url_pesquisa_sap = self.get_full_url(bs_obj2.find("a", text="Matrícula SAP").get('href'))

        obj_pesquisa_rg = self.getBsObject(url_pesquisa_rg)
        page_pesquisa_rg = self.get_full_url(obj_pesquisa_rg.find("input",{"name":"procura"}).get('onclick'))
        
        obj_pesquisa_rg_resultado = self.getBsObject(page_pesquisa_rg)
        url_page_dados = self.get_full_url(obj_pesquisa_rg_resultado.find_all('a', {'class':'textotab1'})[0].get('href'))
        
        obj_dados = self.getBsObject(url_page_dados)
        obj_dados_values = obj_dados.find('table',{'class':'table compact'}).find_all('tr')
        for td in obj_dados_values:
            for i in td:
                print(i)
                # if i.find('span').getText() > -1:
                    # print(i.get('class'))
        # for i in obj_dados_values:
        #     if(i.getText().find(':') > -1):
        #         print('key: '+i.getText().strip())
    
        return json_response

    def post(self):
        params = request.get_json()
        print("Buscando: " + params['nome_completo'])
        result = self.do_crawler(params['nome_completo'])
        return result       