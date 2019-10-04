# smart-search-crawlers

Esse repositório inclui os cralwers dos seguintes sistemas do MPSP:
 - Arpenp
 - Cadesp
 - Caged
 - Censec
 - Detran
 - Infocrim
 - Jucesp (em desenvolvimento)
 - Siel (em desenvolvimento)
 - Sivec (em desenvolvimento)
 
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

#### Arpenp
Método aceito: ```POST``` <br>
Endpoint: ```/arpenp``` <br>
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

