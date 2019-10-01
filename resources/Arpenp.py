import requests
from flask_restful import Resource
import re
from bs4 import BeautifulSoup
import json

class Arpenp(Resource):
    HOSTNAME = 'http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com'
    SITE_NAME = 'arpensp'
    TARGET_URL = "{}/{}/login.html".format(HOSTNAME,SITE_NAME)
    
    def getBsObject(self, url_next_layer):
        print("Requesting URL: " + url_next_layer)
        # print("\n requesting URL:", url_next_layer)
        res_layer = requests.get(url_next_layer).content
        return BeautifulSoup(res_layer, features="lxml")
    def get_full_url(self, path):
        return '{}/{}/{}'.format(self.HOSTNAME, self.SITE_NAME, path)
    def do_crawler(self):
        bs_obj = self.getBsObject(self.TARGET_URL)

        page2_url = bs_obj.find('img', src='./login_files/logo_CRC_JUD.png').parent.get('href')
        page2_url = self.get_full_url(page2_url)

        bs_obj_page2 = self.getBsObject(page2_url)
        page3_url = bs_obj_page2.find('a', text='Busca na CRC').get('href')
        page3_url = self.get_full_url(page3_url)

        bs_obj_page3 = self.getBsObject(page3_url)
        page4_url = bs_obj_page3.find('form',{'name':'form_busca'}).get('action')
        page4_url = self.get_full_url(page4_url)

        bs_obj_page4 = self.getBsObject(page4_url)
        final_form = bs_obj_page4.find('form',{'name':'form_registro'}).find_all('input')
        dict_inputs = {}
        for k, v in enumerate(final_form):
            dict_inputs[final_form[k].get('name')] = v.get('value')
            
        return dict_inputs

    def post(self):
        result = self.do_crawler()
        return result