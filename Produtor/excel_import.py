import pandas as pd
import numpy as np
from childsafe import ChildSafe


def as_list(value):
    parts = value.split(',') if value is not None else []
    return [part.strip() for part in parts]


def vocabulary_from_excel(file_name: str, sheet_name='Termos PT-BR') -> ChildSafe:
    """
    Loads a Child-Safe vocabulary existing in an Excel spreadsheet file and returns it as a list of ChildSafeTerm
    instances.

    :param file_name: the Excel file name.
    :param sheet_name: the Excel sheet name.
    :return: a list containing all the Child-Safe terms found in the Excel file.
    """

    terms_df = pd.read_excel(file_name, sheet_name=sheet_name).replace({np.nan: None})
    terms_df.columns = [
        'termo', 'relacionamentos', 'termos_relacionados', 'termos_gerais', 'classes', 'equivalentes',
        'definicao', 'eixos', 'recomendado',
        'fontes', 'links', 'criador', 'revisores', 'revisor_textual'
    ]
    terms_df.termo = terms_df.termo.apply(lambda value: value.strip())
    terms_df.classes = terms_df.classes.apply(as_list)
    terms_df.relacionamentos = terms_df.relacionamentos.apply(as_list)
    terms_df.termos_relacionados = terms_df.termos_relacionados.apply(as_list)
    terms_df.termos_gerais = terms_df.termos_gerais.apply(as_list)
    terms_df.equivalentes = terms_df.equivalentes.apply(as_list)
    terms_df.eixos = terms_df.eixos.apply(as_list)
    terms_df.revisores = terms_df.revisores.apply(as_list)
    terms_df.fontes = terms_df.fontes.apply(lambda value: value.strip().split('\n') if value is not None else [])
    terms_df.links = terms_df.links.apply(lambda value: value.strip().split('\n') if value is not None else [])
    terms_df.recomendado = terms_df.recomendado.apply(lambda value: value != 'Não')

    terms = terms_df.to_dict('records')
    return ChildSafe(terms)

