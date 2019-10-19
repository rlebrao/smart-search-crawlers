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

class Jucesp(Resource):
    HOSTNAME = 'http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com'
    SITE_NAME = 'jucesp'   
    TARGET_URL = "{}/{}/index.html".format(HOSTNAME,SITE_NAME)
    
    dirname = os.path.dirname
    PDF_FILES = os.path.join(dirname(dirname(__file__)), 'pdf-files')
    TXT_FILES = os.path.join(dirname(dirname(__file__)), 'txt-files')

    def getBsObject(self, url_next_layer):
        print("\n requesting URL:", url_next_layer)
        res_layer = requests.get(url_next_layer).content
        return BeautifulSoup(res_layer, features="lxml")

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
            filename = os.path.join(dirname(dirname(__file__)), 'img-files/jucesp/page_'+ str(image_counter) +".jpg")
            print(filename)
            # filename = os.path.abspath('page_'+ str(image_counter) +".jpg")
            page.save(filename, 'JPEG')
            image_counter = image_counter + 1

        filelimit = image_counter -1
        outfile =  TXT_file_path
        f = open(outfile, 'a', encoding='utf-8')
        for i in range(1, filelimit +1):
            filename = os.path.join(dirname(dirname(__file__)), "img-files/jucesp/page_"+str(i)+".jpg")
            text = str((pytesseract.image_to_string(Image.open(filename)))) 
            text = text.replace('-\n', '').replace("b'", "").replace(r"\r\n","")
            f.write(text)
        f.close()


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

    def do_crawler(self, cnpj):
        json_response = {}
        bs_obj = self.getBsObject(self.TARGET_URL)
        page2_url = bs_obj.find('form',id='aspnetForm').get('action')
        page2_url = self.get_full_url(page2_url)
    
        bs_obj2 = self.getBsObject(page2_url)
        page3_url = bs_obj2.find('input',{"class":"btcadastro"}).get('onclick')
        page3_url = self.get_full_url(page3_url)

        bs_obj3 = self.getBsObject(page3_url)
        page4_url = bs_obj3.find('a', id="ctl00_cphContent_gdvResultadoBusca_gdvContent_ctl02_lbtSelecionar").get('href')
        page4_url = self.get_full_url(page4_url)

        bs_obj4 = self.getBsObject(page4_url)
        capital_empresa = bs_obj4.find('span', id='ctl00_cphContent_frmPreVisualiza_lblCapital').getText()
        
        json_response['capital'] = str(self.getFieldFromTxt('(?<=R\$\s)(?:(?!\s\().)*', capital_empresa)).strip()
        json_response['nome'] = bs_obj4.find('span', {"class":"titulo-azul16-01"}).getText()

        pdf_file = bs_obj4.find('input',{"class":"btcadastro"}).get('onclick')
        pdf_file_url = self.get_full_url(pdf_file)
        
        PDF_file_path = '{}/{}'.format(self.PDF_FILES, pdf_file)
        TXT_file_path = '{}/jucesp_information.txt'.format(self.TXT_FILES)

        self.ocr_download_content(pdf_file_url, PDF_file_path, TXT_file_path)

        pdf_content = open(TXT_file_path, "r",encoding="utf8")
        txt_content = pdf_content.read()

        json_response['tipo'] = self.getFieldFromTxt('(?<=TIPO\:\s)(?:(?!\;).)*',txt_content)
        json_response['diretoria_socios'] = self.getFieldFromTxt('(?<=DIRETORIA\n\n)(?:(?!\,).)*', txt_content) +","+self.getFieldFromTxt('(?<=PELA EMPRESA\.\n\n)(?:(?!\,).)*',txt_content)
        json_response['cnpj'] = self.getFieldFromTxt("(?<=INSCRIGAO ESTADUAL\n[0-9]{4}\/[0-9]{4}\s)(?:(?!\sre).)*", txt_content)

        return json_response
    def post(self):
        params = request.get_json()
        print("Buscando: " + params['cnpj'])
        result = self.do_crawler(params['cnpj'])
        return result