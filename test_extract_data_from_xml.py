"""
How run: python -m unittest
"""
from datetime import datetime
import unittest
from extract_data_from_xml import extract_nfe_data


class ExtractNFeDataTestInvalidXML(unittest.TestCase):
    def test_invalid_xml(self):
        self.assertEqual(extract_nfe_data(''), None)


class ExtractNFeDataTest(unittest.TestCase):
    def setUp(self):
        self.nfe_data = extract_nfe_data('xml_files_test/procNFe1.xml')

    def test_ide(self):
        expected = dict(chave='44141057860952001769550050058200981143544644',
                        nNF='820000',
                        serie='5',
                        data_emissao=datetime.strptime(
                            '2018-10-06', '%Y-%m-%d').date())
        self.assertEqual(self.nfe_data['ide'], expected)

    def test_emit(self):
        expected = dict(CNPJ='88888888888888',
                        CPF='',
                        xNome='NOME DO EMITENTE',
                        xFant='NOME FANTASIA DO EMITENTE',
                        IE='0858585858',
                        xLgr='RUA ADILIO MUTZEMBERG',
                        nro='555',
                        xBairro='DIST.INDUSTRIAL',
                        cMun='4313300',
                        xMun='NOVA PRATA',
                        UF='RS',
                        CEP='95320000',
                        cPais='1058',
                        xPais='BRASIL',
                        fone='32053000',
                        email='')
        self.assertEqual(self.nfe_data['emit'], expected)

    def test_dest(self):
        expected = dict(CNPJ='22222222222222',
                        CPF='',
                        xNome='DESTINATARIO',
                        xFant='',
                        IE='777777777777',
                        xLgr='RUA SUZIN MARTINI',
                        nro='281',
                        xBairro='SALETTE',
                        cMun='3552205',
                        xMun='SOROCABA',
                        UF='SP',
                        CEP='18105008',
                        cPais='1058',
                        xPais='BRASIL',
                        fone='11111111110',
                        email='financeiro@example.com.br')
        self.assertEqual(self.nfe_data['dest'], expected)

    def test_icmstot(self):
        expected = dict(vNF=13474.18, vProd=12832.53)
        self.assertEqual(self.nfe_data['total'], expected)

    def test_vol(self):
        expected = dict(pesoL=1470.000, pesoB=1526.66)
        self.assertEqual(self.nfe_data['vol'], expected)
