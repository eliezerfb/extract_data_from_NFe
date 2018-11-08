"""
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

"""

import glob
import os
import sys

from core import check_manifesto, insert_nf_transp_temp
from extract_data_from_xml import extract_nfe_data

from tkinter import filedialog, messagebox

if len(sys.argv) != 2:
    print('Informe o ID do manifesto como parâmetro')
    sys.exit()

manifesto_id = sys.argv[1]

if check_manifesto(manifesto_id):
    directory = filedialog.askdirectory()
    if os.path.isdir(directory):
        for file in glob.glob(r'{}\*.xml'.format(directory)):
            nfe = extract_nfe_data(file)
            insert_nf_transp_temp(manifesto_id=manifesto_id,
                                  nfe_dict=nfe,
                                  file_name=file)

        messagebox.showinfo('Importação de Notas',
                            'A importação foi concluída.')
