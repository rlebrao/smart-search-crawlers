import requests
from flask_restful import Resource
import re
from bs4 import BeautifulSoup
import json
from flask import jsonify, request

class Cadesp(Resource):
    HOSTNAME = 'http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com'
    SITE_NAME = 'cadesp'
    TARGET_URL = "{}/{}/login.html".format(HOSTNAME,SITE_NAME)
    
    def getBsObject(self, url_next_layer):
        print("Requesting URL: " + url_next_layer+'\n')
        # print("\n requesting URL:", url_next_layer)
        res_layer = requests.get(url_next_layer).content
        return BeautifulSoup(res_layer, features="lxml")

    def get_full_url(self, path):

        return '{}/{}/{}'.format(self.HOSTNAME, self.SITE_NAME, path)

    def do_crawler(self, cnpj):
        bs_obj = self.getBsObject(self.TARGET_URL)
        page2_url = bs_obj.find('form',{'name':'aspnetForm'}).get('action')
        page2_url = self.get_full_url(page2_url)
        
        bs_obj2 = self.getBsObject(page2_url)
        page3_url = bs_obj2.find('a',text="Cadastro").get('href')
        page3_url = self.get_full_url(page3_url)
                
        bs_obj3 = self.getBsObject(page3_url)
        page4_url = bs_obj3.find('form',{'name':'aspnetForm'}).get('action')
        page4_url = self.get_full_url(page4_url) + "?txtIdentificacao="+ cnpj
        
        bs_obj4 = self.getBsObject(page4_url)

        #DADOS CAPTURADOS DO CABEÇALHO DA TABELA
        list_keys_head = bs_obj4.find('table',{'id':'ctl00_conteudoPaginaPlaceHolder_dlCabecalho'}).find_all('td',{'class':'labelDetalhe'})
        list_values_head = bs_obj4.find('table',{'id':'ctl00_conteudoPaginaPlaceHolder_dlCabecalho'}).find_all('td',{'class':'dadoDetalhe'})
        list_keys_normal = []
        list_values_normal = []
        list_keys_outliers = []
        list_vallues_outliers = []
        for i in list_keys_head:
            list_keys_normal.append(i.get_text().strip().replace(':',''))
        for i in list_values_head:
            normalized_item = i.get_text().strip().replace('\t','').replace('\n','').replace('\xa0','').replace('tPFC-10','')
            if( normalized_item != "" and ":" not in normalized_item):
                list_values_normal.append(normalized_item)
            elif(normalized_item.find(':') > -1):
                temp_list = normalized_item.split(':')
                list_keys_outliers.append(temp_list[0])
                list_vallues_outliers.append(temp_list[1])
        
        list_final_keys = list_keys_normal + list_keys_outliers
        list_final_values = list_values_normal + list_vallues_outliers
        count = 0
        dict_response_head = {}
        for k in list_final_keys:
            dict_response_head[k] = list_final_values[count]
            count = count +1


        #DADOS TABELA INFERIOR
        list_keys_head = bs_obj4.find('table',{'id':'ctl00_conteudoPaginaPlaceHolder_dlEstabelecimentoGeral'}).find_all('td',{'class':'labelDetalhe'})
        list_values_head = bs_obj4.find('table',{'id':'ctl00_conteudoPaginaPlaceHolder_dlEstabelecimentoGeral'}).find_all('td',{'class':'dadoDetalhe'})
        list_keys_normal = []
        list_values_normal = []
        list_keys_outliers = []
        list_vallues_outliers = []
        for i in list_keys_head:
            normalized_item = i.get_text().strip().replace('\t','').replace('\n','').replace('\xa0','').replace('tPFC-10','')
            if(normalized_item != "" and normalized_item.find("Nome Fantasia") == -1):
                list_keys_normal.append(i.get_text().strip().replace(':',''))

        for i in list_values_head:
            normalized_item = i.get_text().strip().replace('\t','').replace('\n','').replace('\xa0','').replace('tPFC-10','')
            if(normalized_item != ""):
                if(":" not in normalized_item):
                    list_values_normal.append(normalized_item)
                elif(normalized_item.find(':') > -1):
                    temp_list = normalized_item.split(':')
                    list_keys_outliers.append(temp_list[0])
                    list_vallues_outliers.append(temp_list[1])

        list_final_keys = list_keys_normal + list_keys_outliers
        list_final_values = list_values_normal + list_vallues_outliers
        count = 0
        dict_response_body = {}
        dict_final_response = {}
        for k in list_final_keys:
            dict_response_body[k] = list_final_values[count]
            count = count +1
        dict_final_response.update(dict_response_head)
        dict_final_response.update(dict_response_body)
        return dict_final_response
    
    def post(self):
        params = request.get_json()
        result = self.do_crawler(params['cnpj'])
        return result