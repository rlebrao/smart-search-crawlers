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

class Infocrim(Resource):
    HOSTNAME = 'http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com'
    SITE_NAME = 'infocrim'
    TARGET_URL = "{}/{}/login.html".format(HOSTNAME,SITE_NAME)
    PDF_FILES = "pdf-files"
    TXT_FILES = "txt-files"

    def getBsObject(self, url_next_layer):
        print("Requesting URL: " + url_next_layer+'\n')
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
        for page in PDF_pages:
            print("Converting to .png...")
            filename = "page_" + str(image_counter) +".jpg"
            page.save(filename, 'JPEG')
            image_counter = image_counter + 1

        filelimit = image_counter -1
        outfile =  TXT_file_path
        f = open(outfile, 'a', encoding='utf-8')
        for i in range(1, filelimit +1):
            filename = "page_"+str(i)+".jpg"
            text = str((pytesseract.image_to_string(Image.open(filename)))) 
            text = text.replace('-\n', '').replace("b'", "").replace(r"\r\n","")
            f.write(text)
        f.close()

    def getFieldFromTxt(self, _regex, txt_content):
        try:
            return re.search(_regex, str(txt_content)).group()
        except:
            return ""

    def do_crawler(self):
        bs_obj = self.getBsObject(self.TARGET_URL)
        page2_url = bs_obj.find('img',{'alt':'Envia dados'}).find_parent("a").get("href")
        page2_url = self.get_full_url(page2_url) 
        print(page2_url)   
        return ""
    def post(self):
        params = request.get_json()
        print("Buscando: " + params['cpf'])
        try:
            if params['isTest']:
                isTest = True
        except Exception as e:
            isTest = False
        result = self.do_crawler()
        return result