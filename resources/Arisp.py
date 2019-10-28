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
class Arisp(Resource):

    target_url = "http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com/arisp/login.html"

    HOSTNAME = 'http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com'
    site = 'arisp'

    def getBsObject(self, url_next_layer):
        print("Requesting URL: " + url_next_layer)
        # print("\n requesting URL:", url_next_layer)
        res_layer = requests.get(url_next_layer).content
        return BeautifulSoup(res_layer, features="lxml")

    def getRgDocument(self, str_text):
        infos = re.findall(r'RG.+?(?=e|CPF|\))',str_text)
        normalized_list = []
        for i in infos:
            normalized_document = re.sub(r'n\\\\|xb0|x|\,|RG|SSP\-MS|\\|975|c2|n|\\s','',i)
            normalized_list.append(normalized_document)
        return normalized_list

    def getCPFDocument(self, str_text):
        infos = re.findall(r'CPF.+?(?=e|\))',str_text)
        normalized_list = []
        for i in infos:
            has_numbers = re.search('[0-9]', i)
            is_cpf = re.search('([0-9]{2}[\.|\s]?[0-9]{3}[\.|\s]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.|\s]?[0-9]{3}[\.|\s]?[0-9]{3}[-]?[0-9]{2})', i)
            if(has_numbers and is_cpf):
                normalized_document = re.sub(r'n\\\\|xb0|x|\,|RG|SSP\-MS|\\|975|c2|n|\\s|[^\d,.]+','',i)
                normalized_list.append(normalized_document)
        return normalized_list
    def getAddresses(self, str_text):
        infos = re.search(r'(Rua).+(\d{1,4})',str_text)
        normalized_list = infos
        return normalized_list

    def processText(self, file):
        dict_matricula_info = {}
        with open(file, "rb") as myfile:
            str_line = ""
            for k, v in enumerate(myfile):
                v = str(v).replace(r'b','').replace(r"\r\n", '')
                # print("Line {} : {}".format(k,v))
                str_line = str_line + " " + v.replace(r"'","")
            print(str_line)     
            data_to_read = "".join(str_line)
        #Get RG
        rg_list =self.getRgDocument(data_to_read)
        #Get CPF
        cpf_list = self.getCPFDocument(data_to_read)
        #Get Addresses
        # add_list = self.getAddresses(data_to_read)

        dict_matricula_info['rg'] = rg_list
        dict_matricula_info['cpf'] = cpf_list
        # dict_matricula_info['enderecos'] = add_list
        print(dict_matricula_info)
        return dict_matricula_info

    def do_crawler(self, cpf):
        #First Layer
        c = self.getBsObject(self.target_url)
        url_escolher_estado = c.form.get('action')
        url_next_layer = ("{}/{}/"+url_escolher_estado).format(self.HOSTNAME, self.site)

        #Second Layer
        page_estado = self.getBsObject(url_next_layer)
        url_tipo_pesquisa = page_estado.find('a', text='Solicitações').get('href')
        url_next_layer = ("{}/{}/"+url_tipo_pesquisa).format(self.HOSTNAME, self.site)

        #Third Layer
        page_tipo_pesquisa = self.getBsObject(url_next_layer)
        url_next_layer = page_tipo_pesquisa.find('button',id='Prosseguir').get('onclick')
        url_next_layer = re.sub(r"location\.href\=|\'|\;","",url_next_layer)
        url_next_layer = ("{}/{}/"+url_next_layer).format(self.HOSTNAME, self.site)

        #Forth Layer
        page_selecionar_regiao = self.getBsObject(url_next_layer)
        url_next_layer = page_selecionar_regiao.find('button', id="Prosseguir").get('onclick')
        url_next_layer = re.sub(r"location\.href\=|\'|\;","",url_next_layer)
        url_next_layer = ("{}/{}/"+url_next_layer).format(self.HOSTNAME, self.site)

        #Fifth Layer
        page_escolher_cartorio = self.getBsObject(url_next_layer)
        url_next_layer = page_escolher_cartorio.find('button', id="btnPesquisar").get('onclick')
        url_next_layer = re.sub(r"location\.href\=|\'|\;","",url_next_layer)
        url_next_layer = ("{}/{}/"+url_next_layer).format(self.HOSTNAME, self.site)

        #Sixth Layer
        page_retorno_cpf = self.getBsObject(url_next_layer)
        url_next_layer = page_retorno_cpf.find('button', id="btnProsseguir").get('onclick')
        url_next_layer = re.sub(r"location\.href\=|\'|\;","",url_next_layer)
        url_next_layer = ("{}/{}/"+url_next_layer).format(self.HOSTNAME, self.site)

        #Seventh Layer
        page_matriculas = self.getBsObject(url_next_layer)
        matriculas = page_matriculas.find_all('script')
        count_i_matriculas = 0
        for i in matriculas :
            try:
                if("Site.VM.Loader" in i.get('src')):
                    url_file = matriculas[count_i_matriculas].get('src')
                    pass
            except:
                pass
            count_i_matriculas = count_i_matriculas + 1
        url_next_layer = re.sub(r"\.\/","",url_file) 
        url_next_layer = ("{}/{}/"+url_next_layer).format(self.HOSTNAME, self.site)

        #Eighth Layer
        js_file_page = self.getBsObject(url_next_layer)
        str_matricula_url = "pagina10-visualizar-matriculas.htm"
        if str_matricula_url in str(js_file_page):
            url_next_layer = ("{}/{}/"+str_matricula_url).format(self.HOSTNAME, self.site)
            file_page = self.getBsObject(url_next_layer)
            url_pdf_matricula = file_page.find('img').parent.get('href')
            url_next_layer = re.sub(r"\.\/","",url_pdf_matricula) 
            pdf_url = ("{}/{}/"+url_next_layer).format(self.HOSTNAME, self.site)
            return pdf_url

    def post(self):
        params = request.get_json()
        if(not util.checkAuthorization(request.headers)):
            return {"message": "ERROR: Chave de acesso inválida"}, 401
        else:
            json_response = {}
            if 'cpf' not in params:
                return {"message":"Parâmetro inválido"}, 400
            else:
                json_response['link_para_pdf'] = self.do_crawler(params['cpf'])
                return json_response
