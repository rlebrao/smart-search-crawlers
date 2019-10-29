# smart-search-crawlers

Esse repositório inclui os cralwers dos seguintes sistemas do MPSP:
 - Arpenp
 - Cadesp
 - Caged
 - Censec
 - Detran
 - Infocrim
 - Jucesp 
 - Siel 
 - Sivec 
 
 Sistemas Adicionais:
 - Bolsa família
 - Escavador
 - Jusbrasil

## Dependências
Python >= 3.6 <br>
pip >= 19.0.0

## Instalação
Para instalação, basta realizar o download desse repositório, e com o gerenciador de pacotes pip, executar o seguinte comando para a instalação de todas as dependências:
```shell
pip install -r requirements.txt
```
 
## Inicialização
Para iniciar o serviço, basta executar o seguinte comando na pasta root do projeto:
```shell
python app.py
```
Após isso, o serviço já estará funcionando na porta 5000
![](https://i.imgur.com/xwKKLIt.png)
<br>
Obs: Para o funcionamento correto do comando acima, o python deve estar configurado nas variáveis de ambiente de seu sistema

## Funcionamento
Para cada site do MPSP, existe um endpoint já configurado:
 - Arpenp -> ```shell localhost:5000/arpenp```
 - Cadesp -> ```shell localhost:5000/cadesp```
 - Caged -> ```shell localhost:5000/caged```
 <br> 
 E assim para os demais enpoints...
 
 ### Realizando requisição
Cada endpoint do projeto, possui seus próprios parâmetros que deverão ser passados, assim como cada enpoint possui seu próprio json de retorno

---
#### Arisp
Método aceito: ```POST``` <br>
Endpoint: ```/api/arisp``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```cpf``` <br>

Retorno:
```javascript
{
    "link_para_pdf":"[URL para página da escritura]"
}
```

---


#### Arpenp
Método aceito: ```POST``` <br>
Endpoint: ```/api/arpenp``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```cnpj``` <br>

Retorno:
```javascript
{
    "cartorio_id": "[IDENTIFICADOR DO CARTORIO]",
    "busca_juiz_id": "[IDENTIFICADOR DO JUÍZ]",
    "tipo_registro": "[IDENTIFICADOR TIPO DO REGISTRO]",
    "nome_registrado_1": "[NOME DO PRIMEIRO REGISTRADO]",
    "nome_registrado_2": "[NOME DO SEGUNDO REGISTRADO]",
    "data_ocorrido": "[DATA DO PROCESSO OCORRIDO]",
    "data_registro": "[DATA DO REGISTRO DO PROCESSO]",
    "num_livro": "[NÚMERO DO LIVRO]",
    "num_folha": "[NÚMERO DA FOLHA]",
    "num_registro": "[NÚMERO DE REGISTRO]",
    "matricula": "[NUMERO DE MATRICULA]",
    "nome_requerente": "[NOME DO REQUERENTE]",
    "documento_requerente": "[DOCUMENTO DO REQUERENTE]",
    "telefone_requerente": "[TELEFONE DO REQUERENTE]",
}
```


---

#### Bolsa Família
Método aceito: ```POST``` <br>
Endpoint: ```/api/bolsa-familia``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```nis```, ```ano_mes_referencia```, ```ano_mes_competencia``` <br>

Retorno:
```javascript
{
  "id": [IDENTIFICADOR],
  "dataMesCompetencia": "[DIA/MÊS/ANO]",
  "dataMesReferencia": "[DIA/MÊS/ANO]",
  "titularBolsaFamilia": {
    "nis": "[NÚMERO NIS]",
    "nome": "[NOME COMPLETO]",
    "multiploCadastro": [BOOLEANO INDICANDO MULTIPLOS CADASTROS],
    "cpfFormatado": "***.[TRECHO DO CPF]-**"
  },
  "municipio": {
    "codigoIBGE": "[CÓDIGO DO IBGE]",
    "nomeIBGE": "[NOME DA UNIDADE DO IBGE]",
    "pais": "[PAÍS]",
    "uf": {
      "sigla": "[SIGLA DO ESTADO]",
      "nome": "[NOME DO ESTADO]"
    }
  },
  "valor": [VALOR RECEBIDO],
  "quantidadeDependentes": [QUANTIDADE DE DEPENDENTES CADASTRADOS]
}

```

---


#### Caged
Método aceito: ```POST``` <br>
Endpoint: ```/api/caged``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```cpf``` ou ```cnpj```, <br>

Retorno:
```javascript
{
  "autorizado_responsavel": {
    "identificacao": {
      "cnpj": "[CNPJ DA EMPRESA]",
      "razao_social": "[RAZÃO SOCIAL DA EMPRESA]"
    },
    "dados_cadastrais_atualizados": {
      "logradouro": "[LOGRADOURO]",
      "bairo_distrito": "[BAIRRO CONCATENADO COM DISTRITO]",
      "municipio": "[MUNICIPIO CADASTRADO]",
      "uf": "[ESTADO CADASTRADO]",
      "cep": "[NÚMERO DO CEP DO ENDEREÇO CADASTRADO"]
    },
    "contato": {
      "nome": "[NOME DO CONTATO]",
      "cpf": "[CPF DO CONTATO]",
      "telefone": "TELEFONE DO CONTATO",
      "email": "[EMAIL DO CONTATO]"
    }
  },
  "dados_da_empresa": {
    "cnae": "[NUMERO CNAE DA EMPRESA]"
  },
  "totais": {
    "num_admissoes": "[NÚMERO DE ADMISSOES DA EMPRESA]",
    "variacao_absoluta": "[DIFERENÇA NO DNÚMERO DE FUNCIONÁRIOS DA EMPRESA, DO ÚLTIMO DIA COM O PRIMEIRO DIA]",
    "total_vinculos": "[NÚMERO TOTAL DE VÍNVULOS DA EMPRESA]",
    "desligamentos": "[NÚMERO DE FUNCIONÁRIOS DESLIGADOS DA EMPRESA]",
    "num_primeiro_dia": "[QUANTIDADE DE FUNCIONÁRIOS NO PRIMEIRO DIA DE EMPRESA]",
    "num_ultimo_dia": "[QUANTIDADE DE FUNCIONÁRIOS NO ÚLTIMO DIA DE EMPRESA]"
  },
  "ultima_atualizacao": "[DATA DA ÚLTIMA ATUALIZAÇÃO]",
  
  "identificacao": {
    "nome": "[NOME COMPLETO DO TRABALHADOR]",
    "pis": "[NÚMERO DO PIS]"
  },
  "dados_cadastrais": {
    "cpf": "[CPF DO  TRABALHADOR]",
    "data_nascimento": "[DATA DE NASCIMENTO DO TRABALHADOR]",
    "ctps": "[CATEGORIA DO CTPS]",
    "situacao_pis": "[SITUAÇÃO ATUAL DO PIS DO TRABALHADOR]",
    "nacionalidade": "[NACIONALIDADE DO TRABALHADOR]",
    "escolaridade": "[GRAU DE ESCOLARIDADE DO TRABALHADOR]"
  },
  "tempo_trabalho": {
    "caged": "[NÚMERO DE MESES CADASTRADO NO CAGED]",
    "rais": "[NÚMERO DE MESES DE TRABALHO]"
  },
  "historico_trabalho": {
    "[INDICE]": {
      "fonte": "[FONTE DO HISTÓRICO]",
      "razao social": "[RAZAO SOCIAL DA EMPRESA RESPONSÁVEL PELO HISTÓRICO]",
      "cnpj": "[CNPJ SOCIAL DA EMPRESA RESPONSÁVEL PELO HISTÓRICO]",
      "cei": "[CEI SOCIAL DA EMPRESA RESPONSÁVEL PELO HISTÓRICO]",
      "entrada": "[DATA DE ENTRADA DO TRABALHADOR]",
      "saida": "[DATA DE SAÍDA DO TRABALHADOR]",
      "situacao": "[SITUAÇÃO DO HISTÓRICO]"
    }
  }
}

```

---
#### Cadesp
Método aceito: ```POST``` <br>
Endpoint: ```/api/caged``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```cnpj``` <br>

Retorno:
```javascript
{
    "IE": "[NÚMERO IE DA EMPRESA]",
    "CNPJ": "[NÚMERO CNPJ DA EMPRESA]",
    "Nome Empresarial": "[RAZÃO SOCIAL DA EMPRESA]",
    "DRT": "[CATEGORIA DRT]",
    "Situação": "[SITUAÇÃO DA EMPRESA]",
    "Data da Inscrição no Estado": "[DATA DA INSCRIÇÃO NO ESTADO]",
    "Regime Estadual": "[SIGLA DO REGIME ESTADUAL]",
    "Posto Fiscal": "[POSTO FISCAL DA EMPRESA]",
    "Data Início da IE": "[DATA DE INICIO DO IE DA EMPRESA]",
    "NIRE": "[NÚMERO NIRE]",
    "Situação Cadastral": "[SITUAÇÃO CADASTRAL DA EMPRESA]",
    "Data Início da Situação": "[DATA DE INICIO DA SITUAÇÃO CADASTRAL]",
    "Ocorrência Fiscal": "[OCORRÊNCIA FISCAL DA EMPRESA]",
    "Tipo de Unidade": "[TIPO DA UNIDADE DA EMPRESA]",
    "Formas de Atuação": "[FORMA DE ATUAÇÃO DA EMPRESA]"
}
```
---


#### Censec
Método aceito: ```POST``` <br>
Endpoint: ```/api/censec``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```cnpj``` <br>


Retorno:
```javascript
{
    "dados_cartorio": {
        "ato": {
            "tipo": "[TIPO DO REGISTRO ENCONTRADO]",
            "data": "[DATA DO REGISTRO]"
        },
        "contato": {
            "info": {
                "[INDICE]": {
                    "Telefone": "[TELEFONE DO CONTATO]",
                    "Tipo": "[TIPO DO TELEFONE DO CONTATO]",
                    "Ramal": "[RAMAL DO CONTATO]",
                    "Contato": "[LOCAL DO TELEFONE]",
                    "Status": "[STATUS DO CONTATO]"
                }
            },
            "UF": "[ESTADO DO CONTATO]",
            "municipio": "[MUNICÍPIO DO CONTATO]",
            "nome_cartorio": "[NOME DO CARTÓRIO DO CONTATO]"
        }
    }
}
```

---

#### Detran
Método aceito: ```POST``` <br>
Endpoint: ```/api/detran``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```cnpj``` <br>

Retorno:
``` javascript
{
    "condutor_nome": "[NOME DO CONDUTOR]",
    "condutor_data_nascimento": "[DATA DE NASCIMENTO DO CONDUTOR]",
    "condutor_nascionalidade": "[NASCIONALIDADE DO CONDUTOR]",
    "condutor_cidade_natal": "[CIDADE NATAL DO CONDUTOR]",
    "condutor_rg": "[RG DO CONDUTOR]",
    "condutor_uf": "[SIGLA DO ESTADO DO CONDUTOR]",
    "cnh_registro": "[NÚMERO DE REGISTRO DA CNH DO CONDUTOR]",
    "cnh_local": "[LOCALIDADE DA CNH]",
    "cnh_espelho_pid": "[PID DA CNH]",
    "cnh_data_emissao": "[DATA DE EMISSAO DA CNH]",
    "cnh_status": "[STATUS DA CNH]",
    "cnh_data_primeira_hab": "[DATA DA PRIMEIRA HABILITAÇÃO]",
    "cnh_renach": "[NÚMERO RENACH DO CONDUTOR]",
    "cnh_validade": "[VALIDADE DA CNH]",
    "url_cnh_avatar": "[URL DA IMAGEM DA CNH DO CONDUTOR]",
    "url_cnh_assinatura": "[URL DA IMAGEM DA ASSINATURA DO CONDUTOR]",
    "condutor_nome_pai": "[NOME DO PAI DO CONDUTOR]",
    "condutor_nome_mae": "[NOME DA MÃE DO CONDUTOR]",
    "condutor_cpf": "[CPF DO CONDUTOR]"
}
```

---

#### Escavador 
Método aceito: ```POST``` <br>
Endpoint: ```/api/escavador``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```term ``` <br>

Retorno:
``` javascript
[
    {
        "tipo_resultado": "[TIPO DO RESULTADO ENCONTRADO]",
        "diario_id": [IDENTIFICADOR DO DIÁRIO],
        "numero_pagina": [NÚMERO DE PÁGINAS RETORNADAS],
        "diario_sigla": "[SIGLA DO DIÁRIO]",
        "diario_nome": "[NOME DO DIÁRIO]",
        "diario_data": "[DATA DO DIÁRIO]",
        "caderno": "[CADERNO EM QUE O DIÁRIO SE ENCONTRA]",
        "caderno_url": "[URL DO CADERNO]",
        "texto": "[TEXTO DE AMOSTRA]",
        "link": "[URL PARA O DIÁRIO]",
        "link_api": "[URL PARA CONSULTAR DIÁRIO NA API]"
    },
    {
        "tipo_resultado": "[TIPO DO RESULTADO]",
        "numero_pagina": [NUMERO DE PÁGINAS RETORNADAS],
        "envolvidos_patente": [
            {
                "tipo": "[TIPO DA PATENTE]",
                "nome": "[NOME]",
                "url_id": [ID_URL],
                "slug": "[TIPO SLUG]"
            },
        ],
        "patente_id": [IDENTIFICADOR DA PATENTE]
    }
]
```
---

#### Infocrim 
Método aceito: ```POST``` <br>
Endpoint: ```/api/infocrim``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```cpf``` <br>

Retorno:
```javascript
{
    "crime": {
        "natureza": "[TIPO DO CRIME]",
        "local": "[LOCALIZAÇÃO DO CRIME OCORRIDO]",
        "complemento": "[COMPLEMENTO SOBRE O CRIME]",
        "tipo_local": "[LOCAL DO CRIME]",
        "data_ocorrencia": "[DATA DA OCORRÊNCIA DO CRIME]",
        "data_comunicacao": "[DATA DA COMUNICAÇÃO DO CRIME]"
    }
}
```
---
####  Jusbrasil
Método aceito: ```POST``` <br>
Endpoint: ```/api/jusbrasil``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```cpf ``` <br>

Retorno:
```javascript
{
    "citacoes_encontrados": {
        "[INDICE]": {
            "Diário": "[NOME DO DIÁRIO]",
            "url": "[URL DO DIÁRIO]"
        }
    }
}
```
---

### Juscesp
Método aceito: ```POST``` <br>
Endpoint: ```/api/juscesp``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```cpf ``` <br>

Retorno:

---
### Siel
Método aceito: ```POST``` <br>
Endpoint: ```/api/siel``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```nome_completo ``` <br>

Retorno:

```javascript
{
    "Nome": "[NOME DO ELEITOR]",
    "Título": "[TITULO DO ELEITOR]",
    "Data Nasc.": "[DATA NASCIMENTO DO ELEITOR]",
    "Zona": "[ZONA DO ELEITOR]",
    "Endereço": "[ENDEREÇO DO ELEITOR]",
    "Município": "[CIDADE DO ELEITOR]",
    "UF": "[UF DO LOCAL DE VOTAÇÃO]",
    "Data Domicílio": "[DATA DO DOMICÍLIO]",
    "Nome Pai": "[NOME DO PAI DO ELEITOR]",
    "Nome Mãe": "[NOME DA MÃE DO ELEITOR]",
    "Naturalidade": "[NATURALIDADE DO ELEITOR]",
    "Cód. Validação": "[CÓDIGO DE VALIDAÇÃO DO ELEITOR]"
}
```
---
### Sivec
Método aceito: ```POST``` <br>
Endpoint: ```/api/sivec``` <br>
Headers: ```Content-Type:aplication/json``` <br>
Parâmetros: ```nome_completo ``` <br>

Retorno:
``` javascript
{
    "Nome:": "[NOME CADASTRADO NA CERTIDÃO]",
    "Sexo:": "[SEXO]",
    "Data Nascimento:": "DATA DE NASCIMENTO",
    "RG:": "[NÚMERO DO RG]",
    "Nº controle VEC:": "[NÚMERO DE CONTROLE]",
    "Tipo de RG:": "[TIPO DO RG]",
    "Data Emissão RG:": "[DATA DA EMISSÃO DO RG]",
    "Estado Civil:": "[ESTADO CIVIL]",
    "Naturalidade:": "[NATURALIDADE]",
    "Naturalizado(s/n):": "[SIM OU NÃO CASO SEJA NATURALIZADO]",
    "Posto de Identificação:": "[POSTO DE IDENTIFICAÇÃO]",
    "Grau de Instrução:": "[GRAU DE INSTRUÇÃO]",
    "Nome do Pai:": "[NOME DO PAI]",
    "Cor dos Olhos:": "[COR DOS OLHOS]",
    "Nome da Mãe:": "[NOME DA MÃE]",
    "Cabelo:": "[COR DOS CABELOS]",
    "Cor da Pele:": "[COR DA PELE]",
    "Profissão:": "[PROFISSÃO]"
}
```
