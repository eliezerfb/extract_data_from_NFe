Importação dos dados do XML da NF-e para uma tabela em banco de dados já
existente. Os dados importados serão utilizados para a geração de CT-e
(Conhecimento de Frete Eletrônico) e vinculados a um Manifesto de
Documento Fiscal Eletrônico (MDF-e).

Para configurar o banco de dados é necessário criar um arquivo .env (veja em
.env_example), com a string de conexão com o banco de dados.

Para instalar as bibliotecas utilizadas neste projeto:
pip install -r requeriments.txt

Para executar é necessário passar como parâmetro o ID do manifesto. Exemplo:

python import_nfe.py 317
