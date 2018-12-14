"""
Função para extrair alguns dados de um XML de uma NF-e.
"""
from datetime import datetime
from xml.etree import ElementTree as ET


NS = {'ns': 'http://www.portalfiscal.inf.br/nfe'}


def parse_xml(file_name):
    try:
        return ET.parse(file_name).getroot()
    except Exception:
        return None


def extract_value_from_tag(node, tags, cast=lambda x: x):
    values = {}
    for t in tags:
        tag = node.find(f'ns:{t}', NS)
        values[t] = '' if tag is None else cast(tag.text)
    return values


def extract_ide(infNFe):
    ide = infNFe.find('ns:ide', NS)
    tags = ('nNF', 'serie')
    ide_dict = extract_value_from_tag(node=ide, tags=tags)
    ide_dict['chave'] = infNFe.attrib['Id'][3:]
    ide_dict['data_emissao'] = datetime.strptime(
        ide.find(f'ns:dhEmi', NS).text[:10], '%Y-%m-%d').date()
    return ide_dict


def extract_pn(infNFe, type):
    emit = infNFe.find(f'ns:{type}', NS)
    ender_emit = emit.find(f'ns:ender{type.capitalize()}', NS)
    tags = ('CNPJ', 'CPF', 'xNome', 'xFant', 'IE', 'email')
    emit_dict = extract_value_from_tag(emit, tags)
    tags = ('xLgr', 'nro', 'xBairro', 'cMun', 'xMun', 'UF', 'CEP', 'cPais',
            'xPais', 'fone', 'xCpl')
    ender_emit_dict = extract_value_from_tag(ender_emit, tags)
    emit_dict.update(ender_emit_dict)
    return emit_dict


def extract_total(infNFe):
    total = infNFe.find('ns:total', NS)
    ICMSTot = total.find('ns:ICMSTot', NS)
    tags = ('vNF', 'vProd')
    ICMSTot_dict = extract_value_from_tag(ICMSTot, tags,
                                          cast=lambda x: float(x))
    return ICMSTot_dict


def extract_transp(infNFe):
    transp = infNFe.find('ns:transp', NS)
    tags = ('modFrete', )
    transp_dict = extract_value_from_tag(transp, tags, cast=lambda x: int(x))
    vol = transp.find('ns:vol', NS)
    tags = ('pesoL', 'pesoB', 'qVol')
    vol_dict = extract_value_from_tag(vol, tags, cast=lambda x: float(x))
    return dict(vol_dict, **transp_dict)


def extract_nfe_data(file_name):
    root = parse_xml(file_name)
    if not root:
        return None

    NFe = root.find('ns:NFe', NS)
    infNFe = NFe.find('ns:infNFe', NS)

    return dict(ide=extract_ide(infNFe),
                emit=extract_pn(infNFe, type='emit'),
                dest=extract_pn(infNFe, type='dest'),
                total=extract_total(infNFe),
                transp=extract_transp(infNFe))
