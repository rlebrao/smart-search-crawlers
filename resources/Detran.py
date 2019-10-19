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
class Detran(Resource):
    
    HOSTNAME = 'http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com'
    SITE_NAME = 'detran'
    TARGET_URL = "{}/{}/login.html".format(HOSTNAME,SITE_NAME)
    dirname = os.path.dirname
    PDF_FILES = os.path.join(dirname(dirname(__file__)), 'pdf-files')
    TXT_FILES = os.path.join(dirname(dirname(__file__)), 'txt-files')
    DETRAN_LOG_PATH = os.path.join(dirname(dirname(__file__)),'logs')

    logging.basicConfig(filename=DETRAN_LOG_PATH+"/detran.log")
    def getBsObject(self, url_next_layer):
        print("Requesting URL: " + url_next_layer+'\n')
        # print("\n requesting URL:", url_next_layer)
        res_layer = requests.get(url_next_layer).content
        return BeautifulSoup(res_layer, features="lxml")

    def get_full_url(self, path):

        return '{}/{}/{}'.format(self.HOSTNAME, self.SITE_NAME, path)
    
    def custom_encode_utf8(self, str_input):
        return str_input.replace('\\xc2\\xa','').replace('\\xc3\\xb3','ó').replace('\\xc3\\xa7\\xc3\\xa3','çã').replace("b'0",'').replace('_','').replace("'",'')

    def ocr_download_content(self, pdf_url, PDF_file_path, TXT_file_path):
        r = requests.get(pdf_url, stream=False)
        with open(PDF_file_path,'wb') as f:
            print('Downloading Pdf file...')
            f.write(r.content)
        print("Download completed")
        PDF_pages = convert_from_path(PDF_file_path, 500)
        image_counter = 1
        dirname = os.path.dirname
        for page in PDF_pages:
            print("Converting to .png...")
            filename = os.path.join(dirname(dirname(__file__)), 'page_'+ str(image_counter) +".jpg")
            print(filename)
            # filename = os.path.abspath('page_'+ str(image_counter) +".jpg")
            page.save(filename, 'JPEG')
            image_counter = image_counter + 1

        filelimit = image_counter -1
        outfile =  TXT_file_path
        f = open(outfile, 'a', encoding='utf-8')
        for i in range(1, filelimit +1):
            filename = os.path.join(dirname(dirname(__file__)), "page_"+str(i)+".jpg")
            text = str((pytesseract.image_to_string(Image.open(filename)))) 
            text = text.replace('-\n', '').replace("b'", "").replace(r"\r\n","")
            f.write(text)
        f.close()

    def getFieldFromTxt(self, _regex, txt_content):
        try:
            return re.search(_regex, str(txt_content)).group()
        except:
            return ""

    def do_crawler(self, cnpj, isTest):
        bs_obj = self.getBsObject(self.TARGET_URL)
        page2_url = bs_obj.find('form',{'id':'form'}).get('action')
        page2_url = self.get_full_url(page2_url)

        page2_url = self.getBsObject(page2_url)

        linha_vida_page = page2_url.find('a',id='navigation_a_F_16').get('href')
        linha_vida_page = self.get_full_url(linha_vida_page)

        #First flow
        bs_obj3 = self.getBsObject(linha_vida_page)
        pdf_url = self.get_full_url(bs_obj3.find('span',text="Pesquisar").find_parent('a').get('href'))
        
        #PDF Converting
        PDF_file_path = '{}/{}'.format(self.PDF_FILES, bs_obj3.find('span',text="Pesquisar").find_parent('a').get('href'))
        TXT_file_path = '{}/detran_information.txt'.format(self.TXT_FILES)
        if isTest == False:
            try:
                self.ocr_download_content(pdf_url, PDF_file_path, TXT_file_path)
            except Exception as e:
                logging.error(e)
        pdf_content = open(TXT_file_path, "r")
        txt_content = pdf_content.read()

        #Setting new objects
        json_response = {}        
        #Capturing variables Condutor
        json_response['condutor_nome'] = self.getFieldFromTxt("(?<=Nome do condutor\:)(?:(?!Data Nascimento).)*", txt_content)
        json_response['condutor_data_nascimento'] = self.getFieldFromTxt("(?<=Data Nascimento\:\s).*", txt_content)
        json_response['condutor_nascionalidade'] = self.getFieldFromTxt("(?<=Nacionalidade\:\s)(?:(?!\sNatural).)*", txt_content)
        json_response['condutor_cidade_natal'] = self.getFieldFromTxt("(?<=Natural\:\s).*", txt_content)
        json_response['condutor_rg'] = self.getFieldFromTxt("(?<=RG\:\s)(?:(?!\sUF).)*", txt_content)
        json_response['condutor_uf'] = self.getFieldFromTxt("(?<=UF\:\s).*", txt_content)
        
        #Capturing variables CNH
        json_response['cnh_registro'] = self.getFieldFromTxt("(?<=Registro\:\s)(?:(?!\sPGU).)*", txt_content)
        json_response['cnh_local'] = self.getFieldFromTxt("(?<=Local\:\s)(?:(?!\sCategoria).)*", txt_content)
        json_response['cnh_espelho_pid'] = self.getFieldFromTxt("(?<=Espelho PID\:\s)(?:(?!\?).)*", txt_content)
        json_response['cnh_data_emissao'] = self.getFieldFromTxt("(?<=Emissao CNH\:\s)(?:(?!\sStatus).)*", txt_content)
        json_response['cnh_status'] = self.getFieldFromTxt("(?<=Status CNH\:\s).*", txt_content)
        json_response['cnh_data_primeira_hab'] = self.getFieldFromTxt("(?<=Habilitagao\:\s).*", txt_content)
        json_response['cnh_renach'] = self.getFieldFromTxt("(?<=RENACH\:\s).*", txt_content)
        json_response['cnh_validade'] = self.getFieldFromTxt("(?<=Validade CNH\:\s).*", txt_content)
        #End of first flow

        #Second Flow
        url_consulta_imagem = page2_url.find('ul',id="navigation_ul_M_16").find_all('a')[1].get('href')
        url_consulta_imagem = self.get_full_url(url_consulta_imagem)

        bs_obj4 = self.getBsObject(url_consulta_imagem)
        url_consulta_imagem_next = bs_obj4.find('span',text="Pesquisar").find_parent('a').get('href')
        url_consulta_imagem_next = self.get_full_url(url_consulta_imagem_next)

        bs_obj5 = self.getBsObject(url_consulta_imagem_next)

        json_response['url_cnh_avatar'] = bs_obj5.find("img", id="form:imgFoto").get("src")
        json_response['url_cnh_assinatura'] = self.get_full_url(bs_obj5.find("img", id="form:imgAssinatura").get("src"))
        json_response['condutor_nome_pai'] = bs_obj5.find_all("table")[15].find('span').getText()
        json_response['condutor_nome_mae'] = bs_obj5.find_all("table")[16].find('span').getText()
        json_response['condutor_cpf'] = bs_obj5.find_all("table")[17].find_all("span")[3].getText()

        return json_response

    def post(self):
        params = request.get_json()
        print("Buscando: " + params['cpf'])
        try:
            if params['isTest']:
                isTest = True
        except Exception as e:
            isTest = False
        result = self.do_crawler(params['cpf'], isTest)
        return result
