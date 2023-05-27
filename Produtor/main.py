import excel_import
import json_serializer as json_s
import turtle

import pandas as pd
from childsafe import ChildSafe


def main():
    de_turtle = False
    para_turtle = True
    para_json = True

    child_safe = None
    if de_turtle:
        terms = turtle.read_from('../Ontologia/child-safe.ttl')
        child_safe = ChildSafe(terms)

    if para_turtle or para_json:
        if child_safe is None:
            child_safe = excel_import.vocabulary_from_excel('../../Child-safe.xlsx')
        if para_turtle:
            turtle.save_as(child_safe, '../Ontologia/child-safe.ttl')
        if para_json:
            json_s.export_to_json(child_safe, '../Navegador/js/child-safe.js')


if __name__ == '__main__':
    main()
