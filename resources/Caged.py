import requests
from flask_restful import Resource
import re
from bs4 import BeautifulSoup
import json
from flask import jsonify, request

class Caged(Resource):
    HOSTNAME = 'http://ec2-18-231-116-58.sa-east-1.compute.amazonaws.com'
    SITE_NAME = 'caged'   
    TARGET_URL = "{}/{}/login.html".format(HOSTNAME,SITE_NAME)
    
    def getBsObject(self, url_next_layer):
        print("Requesting URL: " + url_next_layer+'\n')
        # print("\n requesting URL:", url_next_layer)
        res_layer = requests.get(url_next_layer).content
        return BeautifulSoup(res_layer, features="lxml")

    def get_full_url(self, path):
        if path.find('location.href') > -1:
            path = re.sub("location.href='",'',path)
            path = re.sub("'",'',path)
        return '{}/{}/{}'.format(self.HOSTNAME, self.SITE_NAME, path)
        
    def do_crawler_autorizado_responsavel(self, cnpj):
        bs_obj = self.getBsObject(self.TARGET_URL)
        page2_url = bs_obj.find('form',{'id':'fm1'}).get('action')
        page2_url = self.get_full_url(page2_url)

        bs_obj2 = self.getBsObject(page2_url)
        page3_url = bs_obj2.find('a',id="j_idt12:idMenuLinkAutorizado").get('href')
        page3_url = self.get_full_url(page3_url)

        bs_obj3 = self.getBsObject(page3_url)
        page4_url = bs_obj3.find('form',id="j_idt12").get('action')
        page4_url = self.get_full_url(page4_url)
        
        bs_obj4 = self.getBsObject(page4_url)
        dict_response = {}
        dict_response['identificacao'] = {}
        dict_response['dados_cadastrais_atualizados'] = {}
        dict_response['contato'] = {}

        dict_response['identificacao']['cnpj'] = bs_obj4.find('span',id='txCnpj020_2').getText()
        dict_response['identificacao']['razao_social'] = bs_obj4.find('span',id="txtrazaosocial020_4").getText()

        dict_response['dados_cadastrais_atualizados']['logradouro'] = bs_obj4.find('span',id="txt3_logradouro020").getText()
        dict_response['dados_cadastrais_atualizados']['bairo_distrito'] = bs_obj4.find('span',id="txt4_bairro020").getText()
        dict_response['dados_cadastrais_atualizados']['municipio'] = bs_obj4.find('span',id="txt6_municipio020").getText()
        dict_response['dados_cadastrais_atualizados']['uf'] = bs_obj4.find('span',id="txt7_uf020").getText()
        dict_response['dados_cadastrais_atualizados']['cep'] = bs_obj4.find('span',id="txt8_cep020").getText()

        dict_response['contato']['nome'] = bs_obj4.find('span',id="txt_nome_contato").getText()
        dict_response['contato']['cpf'] = bs_obj4.find('span',id="txt_contato_cpf").getText()
        dict_response['contato']['telefone'] = bs_obj4.find('span',id="txt9_telefone020").getText()
        dict_response['contato']['telefone'] = bs_obj4.find('span',id="txt10_ramal020").getText()
        dict_response['contato']['email'] = bs_obj4.find('span',id="txt11_email").getText()
        
        return {'autorizado_responsavel':dict_response}

    def do_crawler_empresa(self, cnpj):
        bs_obj = self.getBsObject(self.TARGET_URL)
        page2_url = bs_obj.find('form',{'id':'fm1'}).get('action')
        page2_url = self.get_full_url(page2_url)
        
        bs_obj2 = self.getBsObject(page2_url)
        page3_url = bs_obj2.find('a',id="j_idt12:idMenuLinkEmpresaCaged").get('href')
        page3_url = self.get_full_url(page3_url)

        bs_obj3 = self.getBsObject(page3_url)
        page4_url = bs_obj3.find('form',id="formPesquisarEmpresaCAGED").get('action')
        page4_url = self.get_full_url(page4_url)

        bs_obj4 = self.getBsObject(page4_url)

        dict_response = {}
        dict_response['dados_da_empresa'] = {}
        dict_response['totais'] = {}

        dict_response['dados_da_empresa']['cnae'] = bs_obj4.find('span',{'id':'formResumoEmpresaCaged:txtCodigoAtividadeEconomica'}).getText()
        
        dict_response['totais']['num_admissoes'] = bs_obj4.find('span',{'id':'formResumoEmpresaCaged:txtTotalNumAdmissoes'}).getText()
        dict_response['totais']['variacao_absoluta'] = bs_obj4.find('span',{'id':'formResumoEmpresaCaged:txtTotalVariacaoAbosulta'}).getText()
        dict_response['totais']['total_vinculos'] = bs_obj4.find('span',{'id':'formResumoEmpresaCaged:txtTotalVinculos'}).getText()
        dict_response['totais']['desligamentos'] = bs_obj4.find('span',{'id':'formResumoEmpresaCaged:txtTotalNumDesligamentos'}).getText()
        dict_response['totais']['num_primeiro_dia'] = bs_obj4.find('span',{'id':'formResumoEmpresaCaged:txtTotalNumPrimDia'}).getText()
        dict_response['totais']['num_ultimo_dia'] = bs_obj4.find('span',{'id':'formResumoEmpresaCaged:txtTotalNumUltDia'}).getText()

        dict_response['ultima_atualizacao'] = bs_obj4.find('span',{'id':'txtCompetencia'}).getText()
        return dict_response
        
    def do_crawler_trabalhador(self, search_key):
        bs_obj = self.getBsObject(self.TARGET_URL)
        page2_url = bs_obj.find('form',{'id':'fm1'}).get('action')
        page2_url = self.get_full_url(page2_url)
        
        bs_obj2 = self.getBsObject(page2_url)
        page3_url = bs_obj2.find('a',id="j_idt12:idMenuLinkTrabalhador").get('href')
        page3_url = self.get_full_url(page3_url)

        bs_obj3 = self.getBsObject(page3_url)
        page4_url = bs_obj3.find('form',id="formPesquisarTrabalhador").get('action')
        page4_url = self.get_full_url(page4_url)


        bs_obj4 = self.getBsObject(page4_url)
        
        json_response = {}
        json_response['identificacao'] = {}
        json_response['dados_cadastrais'] = {}
        json_response['tempo_trabalho'] = {}

        json_response['identificacao']['nome'] = bs_obj4.find('span',id='txt2_Nome027').getText()
        json_response['identificacao']['pis'] = bs_obj4.find('span',id='lb1_pispasep027').getText()

        json_response['dados_cadastrais']['cpf'] = bs_obj4.find('span',id='txt3_Cpf027').getText()
        json_response['dados_cadastrais']['data_nascimento'] = bs_obj4.find('span',id='lb4_datanasc027').getText()
        json_response['dados_cadastrais']['ctps'] = bs_obj4.find('span',id='lb5_Ctps027').getText()
        json_response['dados_cadastrais']['situacao_pis'] = bs_obj4.find('span',id='txt4_SitPis027').getText()
        json_response['dados_cadastrais']['nacionalidade'] = bs_obj4.find('span',id='lb8_Nac027').getText()
        json_response['dados_cadastrais']['escolaridade'] = bs_obj4.find('span',id='txt12_Instr027').getText()
        
        json_response['tempo_trabalho']['caged'] = bs_obj4.find('span',id='txt26_Caged027').getText()
        json_response['tempo_trabalho']['rais'] = bs_obj4.find('span',id='txt27_Rais027').getText()

        #Monta as chaves do dicionário
        dict_table_headers = {}
        list_table_headers = []
        tabela_headers = bs_obj4.find_all('th',{'class':'tabela-header'})

        for header in tabela_headers:
            key = header.find('span').getText().lower().replace('í','i').replace('ã','a').replace('ç','c')
            dict_table_headers[key] = {}
            list_table_headers.append(key)

        #Monta os valores do dicionário
        dict_table_body = {}
        tabela_body = bs_obj4.find('tbody',id='HistoricoMov_Trabalhador_2:panelTabbedPane_resumo_trabalhador_2:movimentos_rais_caged_4:mov_rais_cage:tbody_element').find_all('tr')

        dict_response_historico_trabalho = {}
        for all_rows in tabela_body:
            count_external = 0
            count = 0
            for row in all_rows:
                try:
                    if row.find('span').getText().find('cei') == -1:
                        dict_table_body[list_table_headers[count]] = row.find('span').getText()
                        # print(row.find('span').getText())
                        # print("Key: "+list_table_headers[count])
                        # print('------')
                    else:
                        dict_table_body[list_table_headers[count]] = row.find('span').getText()
                        # print(row.find('span').getText())
                        # print("Key: "+list_table_headers[count])
                        # print('------')
                    dict_response_historico_trabalho[count] = dict_table_body
                    count = count + 1
                except:
                    pass
            
            count_external = count_external + 1
        json_response['historico_trabalho'] = dict_response_historico_trabalho   
        
        return json_response    

    def post(self):
        params = request.get_json()
        json_response = {}
        #CNPJ, CEI, CPF, Razao social ou CREA
        result_autorizado_responsavel = self.do_crawler_autorizado_responsavel(params['cnpj'])
        #Somente CNPJ
        result_empresa = self.do_crawler_empresa(params['cnpj'])
        #CPF, Nome ou PIS
        result_trabalhador = self.do_crawler_trabalhador(params['cpf'])
        json_response = result_autorizado_responsavel.copy()
        json_response.update(result_empresa)
        json_response.update(result_trabalhador)
        return json_response