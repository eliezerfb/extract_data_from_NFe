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
