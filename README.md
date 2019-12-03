# movieQA

## Instalação e uso
Foi utilizado Python 3.7

Intalação dos pacotes utilizados:

`pip install -r requirements.txt`

Para instalar os adicionais do NLTK:

`python main.py -i`

Para rodar:

`python main.py`


## Como funciona

O movieQA é um sistema de respostas de questões de dominio fechado que responde perguntas relacionadas a filmes, atores e diretores.
De forma que o sistema recebe perguntas em linguagem natural (inglês) dentro de alguns padrões sintaticos pré-determinados e responde estas
perguntas através da busca das respostas em queries SPARQL no DBpedia e estruturação destes dados como uma resposta em linguagem natural.

### Processamento das queries

As ações envolvidas no processamento das perguntas são:

* Tokenização
* Remoção de Pontuação
* POS-Tagging
* Lematização
