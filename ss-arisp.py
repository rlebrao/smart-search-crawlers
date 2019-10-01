import requests
import re
from PIL import Image
import pytesseract
import sys
import os
from pdf2image import convert_from_path
import re
from bs4 import BeautifulSoup

target_url = "http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com/arisp/login.html"

hostname = 'http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com'
site = 'arisp'


def getBsObject(url_next_layer):
    print("Requesting URL: " + url_next_layer)
    # print("\n requesting URL:", url_next_layer)
    res_layer = requests.get(url_next_layer).content
    return BeautifulSoup(res_layer, features="lxml")

def getRgDocument(str_text):
    infos = re.findall(r'RG.+?(?=e|CPF|\))',str_text)
    normalized_list = []
    for i in infos:
        normalized_document = re.sub(r'n\\\\|xb0|x|\,|RG|SSP\-MS|\\|975|c2|n|\\s','',i)
        normalized_list.append(normalized_document)
    return normalized_list

def getCPFDocument(str_text):
    infos = re.findall(r'CPF.+?(?=e|\))',str_text)
    normalized_list = []
    for i in infos:
        has_numbers = re.search('[0-9]', i)
        is_cpf = re.search('([0-9]{2}[\.|\s]?[0-9]{3}[\.|\s]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.|\s]?[0-9]{3}[\.|\s]?[0-9]{3}[-]?[0-9]{2})', i)
        if(has_numbers and is_cpf):
            normalized_document = re.sub(r'n\\\\|xb0|x|\,|RG|SSP\-MS|\\|975|c2|n|\\s|[^\d,.]+','',i)
            normalized_list.append(normalized_document)
    return normalized_list
def getAddresses(str_text):
    infos = re.search(r'(Rua).+(\d{1,4})',str_text)
    normalized_list = infos
    return normalized_list
def processText(file):
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
    rg_list = getRgDocument(data_to_read)
    #Get CPF
    cpf_list = getCPFDocument(data_to_read)
    #Get Addresses
    add_list = getAddresses(data_to_read)

    dict_matricula_info['rg'] = rg_list
    dict_matricula_info['cpf'] = cpf_list
    dict_matricula_info['enderecos'] = add_list
    print(dict_matricula_info)

#First Layer
c = getBsObject(target_url)
url_escolher_estado = c.form.get('action')
url_next_layer = ("{}/{}/"+url_escolher_estado).format(hostname, site)

#Second Layer
page_estado = getBsObject(url_next_layer)
url_tipo_pesquisa = page_estado.find('a', text='Solicitações').get('href')
url_next_layer = ("{}/{}/"+url_tipo_pesquisa).format(hostname, site)

#Third Layer
page_tipo_pesquisa = getBsObject(url_next_layer)
url_next_layer = page_tipo_pesquisa.find('button',id='Prosseguir').get('onclick')
url_next_layer = re.sub(r"location\.href\=|\'|\;","",url_next_layer)
url_next_layer = ("{}/{}/"+url_next_layer).format(hostname, site)

#Forth Layer
page_selecionar_regiao = getBsObject(url_next_layer)
url_next_layer = page_selecionar_regiao.find('button', id="Prosseguir").get('onclick')
url_next_layer = re.sub(r"location\.href\=|\'|\;","",url_next_layer)
url_next_layer = ("{}/{}/"+url_next_layer).format(hostname, site)

#Fifth Layer
page_escolher_cartorio = getBsObject(url_next_layer)
url_next_layer = page_escolher_cartorio.find('button', id="btnPesquisar").get('onclick')
url_next_layer = re.sub(r"location\.href\=|\'|\;","",url_next_layer)
url_next_layer = ("{}/{}/"+url_next_layer).format(hostname, site)

#Sixth Layer
page_retorno_cpf = getBsObject(url_next_layer)
url_next_layer = page_retorno_cpf.find('button', id="btnProsseguir").get('onclick')
url_next_layer = re.sub(r"location\.href\=|\'|\;","",url_next_layer)
url_next_layer = ("{}/{}/"+url_next_layer).format(hostname, site)

#Seventh Layer
page_matriculas = getBsObject(url_next_layer)
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
url_next_layer = ("{}/{}/"+url_next_layer).format(hostname, site)

#Eighth Layer
js_file_page = getBsObject(url_next_layer)
str_matricula_url = "pagina10-visualizar-matriculas.htm"
if str_matricula_url in str(js_file_page):
    url_next_layer = ("{}/{}/"+str_matricula_url).format(hostname, site)
    file_page = getBsObject(url_next_layer)
    url_pdf_matricula = file_page.find('img').parent.get('href')
    url_next_layer = re.sub(r"\.\/","",url_pdf_matricula) 
    pdf_url = ("{}/{}/"+url_next_layer).format(hostname, site)
    r = requests.get(pdf_url, stream=False)
    PDF_file_path = 'pdf-files/pagina11-escritura.pdf'
    with open(PDF_file_path,'wb') as f:
        print('Downloading Pdf file...')
        f.write(r.content)
    print("Download completed")
    print("Preparing file for conversion")
    PDF_pages = convert_from_path(PDF_file_path, 500)
    image_counter = 1
    for page in PDF_pages:
        print("Converting to .png...")
        filename = "page_" + str(image_counter) +".jpg"
        page.save(filename, 'JPEG')
        image_counter = image_counter + 1

    filelimit = image_counter -1
    outfile =  "out_text.txt"
    f = open(outfile, 'a', encoding='utf-8')
    for i in range(1, filelimit +1):
        filename = "page_"+str(i)+".jpg"
        text = str((pytesseract.image_to_string(Image.open(filename)))) 
        text = text.replace('-\n', '').replace("b'", "").replace(r"\r\n","")
        f.write(text)
    f.close()
    
else:
    print("\n Matricula não encontrada")
processText(outfile)

    
