from decouple import config
from sqlalchemy import (create_engine, MetaData, Column,
                        Table, Integer, String, Numeric, Date, LargeBinary,
                        select)

engine = create_engine(config('DATABASE_URL'), echo=False)
metadata = MetaData(bind=engine, reflect=False)
conn = engine.connect()

# manifesto = metadata.tables['manifesto']
# nf_transp_temp_table = metadata.tables['nf_transp_temp']
# print(nf_transp_temp_table)


nf_transp_temp_table = Table(
    'nf_transp_temp', metadata,
    Column('manifesto_id', Integer),
    Column('num_doc', Integer),
    Column('serie', String(3)),
    Column('chave_nfe', String(60)),
    Column('remet_razao', String(60)),
    Column('remet_fantasia', String(60)),
    Column('remet_cnpj', String(15)),
    Column('remet_cpf', String(11)),
    Column('remet_ie', String(60)),
    Column('remet_logradouro', String(100)),
    Column('remet_numero', String(10)),
    Column('remet_cidade_nome', String(60)),
    Column('remet_cidade_ibge', String(10)),
    Column('remet_cidade_uf', String(2)),
    Column('dest_razao', String(60)),
    Column('dest_fantasia', String(60)),
    Column('dest_cnpj', String(15)),
    Column('dest_cpf', String(11)),
    Column('dest_ie', String(60)),
    Column('dest_logradouro', String(100)),
    Column('dest_numero', String(10)),
    Column('dest_cidade_nome', String(60)),
    Column('dest_cidade_ibge', String(10)),
    Column('dest_cidade_uf', String(2)),
    Column('dest_email', String(100)),
    Column('valor_nf', Numeric(18, 2)),
    Column('peso_l', Numeric(18, 4)),
    Column('peso_b', Numeric(18, 4)),
    Column('data_emissao', Date()),
    Column('file_name', LargeBinary())
)

manifesto = Table(
    'manifesto', metadata,
    Column('id', Integer)
)


def check_manifesto(id):
    s = select([manifesto]).where(manifesto.c.id == id)
    result = conn.execute(s)
    row = result.fetchone()
    return True if row else False


def insert_nf_transp_temp(manifesto_id, nfe_dict, file_name):
    s = select([nf_transp_temp_table]).\
            where(nf_transp_temp_table.c.manifesto_id == manifesto_id).\
            where(nf_transp_temp_table.c.chave_nfe == nfe_dict['ide']['chave'])
    result = conn.execute(s)
    row = result.fetchone()
    if not row:
        ins = nf_transp_temp_table.insert()
        new_nfe = ins.values(manifesto_id=manifesto_id,
                             serie=nfe_dict['ide']['serie'],
                             num_doc=nfe_dict['ide']['nNF'],
                             data_emissao=nfe_dict['ide']['data_emissao'],
                             chave_nfe=nfe_dict['ide']['chave'],
                             remet_razao=nfe_dict['emit']['xNome'],
                             remet_fantasia=nfe_dict['emit']['xFant'],
                             remet_cnpj=nfe_dict['emit']['CNPJ'],
                             remet_cpf=nfe_dict['emit']['CPF'],
                             remet_ie=nfe_dict['emit']['IE'],
                             remet_logradouro=nfe_dict['emit']['xLgr'],
                             remet_numero=nfe_dict['emit']['nro'][:10],
                             remet_cidade_nome=nfe_dict['emit']['xMun'],
                             remet_cidade_ibge=nfe_dict['emit']['cMun'],
                             remet_cidade_uf=nfe_dict['emit']['UF'],
                             dest_razao=nfe_dict['dest']['xNome'],
                             dest_fantasia=nfe_dict['dest']['xFant'],
                             dest_cnpj=nfe_dict['dest']['CNPJ'],
                             dest_cpf=nfe_dict['dest']['CPF'],
                             dest_ie=nfe_dict['dest']['IE'],
                             dest_logradouro=nfe_dict['dest']['xLgr'],
                             dest_numero=nfe_dict['dest']['nro'][:10],
                             dest_cidade_nome=nfe_dict['dest']['xMun'],
                             dest_cidade_ibge=nfe_dict['dest']['cMun'],
                             dest_cidade_uf=nfe_dict['dest']['UF'],
                             dest_email=nfe_dict['dest']['email'],
                             valor_nf=nfe_dict['total']['vNF'],
                             peso_l=nfe_dict['vol']['pesoL'],
                             peso_b=nfe_dict['vol']['pesoB'],
                             file_name=file_name
                             )

        conn.execute(new_nfe)
