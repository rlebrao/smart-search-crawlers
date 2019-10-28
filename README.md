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
pip install requirements.txt
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
    "codigoIBGE": "[CÓDIGO DO IBGE",
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
