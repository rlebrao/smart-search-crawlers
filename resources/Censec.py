import requests
from flask_restful import Resource
import re
from bs4 import BeautifulSoup
import json
from flask import jsonify, request
from common import util

class Censec(Resource):
    HOSTNAME = 'http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com'
    SITE_NAME = 'censec'
    TARGET_URL = "{}/{}/login.html".format(HOSTNAME,SITE_NAME)
    
    def getBsObject(self, url_next_layer):
        print("Requesting URL: " + url_next_layer+'\n')
        # print("\n requesting URL:", url_next_layer)
        res_layer = requests.get(url_next_layer).content
        return BeautifulSoup(res_layer, features="lxml")

    def get_full_url(self, path):

        return '{}/{}/{}'.format(self.HOSTNAME, self.SITE_NAME, path)
    
    def custom_encode_utf8(self, str_input):
        return str_input.replace('\\xc2\\xa','').replace('\\xc3\\xb3','ó').replace('\\xc3\\xa7\\xc3\\xa3','çã').replace("b'0",'').replace('_','').replace("'",'')

    def do_crawler(self, cnpj):
        bs_obj = self.getBsObject(self.TARGET_URL)
        page2_url = bs_obj.find('input',{'id':'EntrarButton'}).get('onclick').replace("'","").replace(";","").replace("location.href=","")
        page2_url = self.get_full_url(page2_url)
        
        bs_obj2 = self.getBsObject(page2_url)
        page3_url = bs_obj2.find('a',{'id':'ctl00_CESDIConsultaAtoHyperLink'}).get('href')
        page3_url = self.get_full_url(page3_url)

        bs_obj3 = self.getBsObject(page3_url)
        page4_url = bs_obj3.find('form',{'name':'aspnetForm'}).get('action')
        page4_url = self.get_full_url(page4_url)

        bs_obj4 = self.getBsObject(page4_url)
        page5_url = bs_obj4.find('form',{'name':'aspnetForm'}).get('action')
        page5_url = self.get_full_url(page5_url)

        bs_obj5 = self.getBsObject(page5_url)

        json_response = {}
        json_response['dados_cartorio'] = {}
        json_response['dados_cartorio']['ato'] = {}
        json_response['dados_cartorio']['contato'] = {}
        json_response['dados_cartorio']['contato']['info'] = {}
        json_response['dados_cartorio']['contato']['UF'] = bs_obj5.find('input',id="ctl00_ContentPlaceHolder1_DadosCartorio_CartorioUFTextBox")['value']
        json_response['dados_cartorio']['contato']['municipio'] = bs_obj5.find('input',id='ctl00_ContentPlaceHolder1_DadosCartorio_CartorioMunicipioTextBox')['value']
        json_response['dados_cartorio']['contato']['nome_cartorio'] = bs_obj5.find('input',id='ctl00_ContentPlaceHolder1_DadosCartorio_CartorioNomeTextBox')['value']
        

        json_response['dados_cartorio']['ato']['tipo'] = bs_obj5.find('select',id='ctl00_ContentPlaceHolder1_TipoAtoDropDownList').find('option')['value']
        json_response['dados_cartorio']['ato']['data'] = bs_obj5.find('input',id='ctl00_ContentPlaceHolder1_DiaAtoTextBox')['value'] + "/" + bs_obj5.find('input',id='ctl00_ContentPlaceHolder1_MesAtoTextBox')['value'] + "/" + bs_obj5.find('input',id='ctl00_ContentPlaceHolder1_AnoAtoTextBox')['value']

        list_cartorio_keys = []
        cartorio_keys_obj = bs_obj5.find_all('tr',{'class':'titulosTabelas'})[1].find_all('td')
        #Lambda function
        [list_cartorio_keys.append(str(i.renderContents()).replace("'","").replace('b','')) for i in cartorio_keys_obj]
        
        cartorio_values_obj = bs_obj5.find_all('div',{'class':'rolagem'})[1].find_all('tr')
        count = 0
        for i in cartorio_values_obj:
            count_intern_node = 0
            json_response['dados_cartorio']['contato']['info'][count] = {}
            all_td = i.find_all('td')
            for j in all_td:
                json_response['dados_cartorio']['contato']['info'][count][list_cartorio_keys[count_intern_node]] = self.custom_encode_utf8(str(j.encode_contents()))
                count_intern_node = count_intern_node + 1
            count = count +1
            
        return json_response
        
    def post(self):
        if(not util.checkAuthorization(request.headers)):
            return {"message": "ERROR: Chave de acesso inválida"}, 401
        else:
            params = request.get_json()
            print("Buscando: " + params['cnpj'])
            result = self.do_crawler(params['cnpj'])
            return result