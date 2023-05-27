from childsafe import ChildSafe, TermDescriptor
from rdflib import Graph


childsafe_uri_base = 'http://br/mmfdh/ufpr/2022/2/child-safe'
childsafe_uri = f'<{childsafe_uri_base}#>'
childsafe_version = '1.0.0'


def read_from(filename: str) -> list[TermDescriptor]:
    graph = Graph()
    graph.parse(filename, format='ttl')
    subjects = read_terms(graph)
    return subjects


def read_terms(graph: Graph) -> list[dict]:
    def parts_of(uri):
        pieces = uri.split('#')
        if len(pieces) == 2:
            return pieces
        else:
            return None, pieces[0]

    domain_tags = {
        'Criança e Adolescente': 'CA',
        'Direito': 'DI',
        'Geral': 'GE',
        'Saúde': 'SA',
        'Tecnologia': 'TE',
    }
    subjects = dict()
    for subj, pred, obj in graph:
        namespace, name = parts_of(subj)
        if namespace != childsafe_uri_base:
            continue
        if name not in subjects:
            subjects[name] = {
                'termo': name,
                'termos_gerais': [],
                'equivalentes': [],
                'eixos': [],
                'fontes': [],
                'links': [],
                'relacionamentos': [],
                'termos_relacionados': [],
                'classes': [],
            }
        term = subjects[name]

        obj = str(obj)
        namespace, predicate_name = parts_of(pred)
        if predicate_name == 'sameAs':
            namespace, object_name = parts_of(obj)
            term['equivalentes'].append(object_name)
        elif predicate_name == 'subClassOf':
            namespace, object_name = parts_of(obj)
            term['termos_gerais'].append(object_name)
        elif predicate_name == 'type':
            namespace, object_name = parts_of(obj)
            if object_name not in ['Class', 'ObjectProperty', 'AnnotationProperty', 'TransitiveProperty']:
                term['classes'].append(object_name)
        elif predicate_name == 'label':
            term['termo'] = obj
        elif predicate_name == 'comment':
            term['definicao'] = obj
        elif predicate_name == 'definedIn':
            term['eixos'].append(domain_tags[obj])
        elif predicate_name == 'sourceIs':
            term['fontes'].append(obj)
        elif predicate_name == 'linkIs':
            term['links'].append(obj)
        elif predicate_name == 'isRecommendedTerm':
            term['recomendado'] = obj != 'Não'
        else:
            if namespace == childsafe_uri_base:
                namespace, object_name = parts_of(obj)
                term['relacionamentos'].append(predicate_name)
                term['termos_relacionados'].append(object_name)

    subjects = [term for term in list(subjects.values()) if len(term['eixos']) > 0]
    subjects.sort(key=lambda item: item['termo'])
    return subjects


def ttl_heading():
    with open('heading.ttl', 'r', encoding='UTF-8') as f:
        content = f.read()
    content = content\
        .replace('{childsafe_uri}', childsafe_uri)\
        .replace('{childsafe_uri_base}', childsafe_uri_base)\
        .replace('{childsafe_version}', childsafe_version)
    return content.split('\'n')


def as_turtle(childsafe: ChildSafe) -> str:
    content = ttl_heading()
    _add_base_constructs(content, childsafe)

    for item in childsafe.items:
        if item.name[0] == '*':
            continue
        _append_class(content, item)
        _append_individual(content, item)

    return '\n'.join(content)


def save_as(childsafe: ChildSafe, file_name: str):
    content = as_turtle(childsafe)
    with open(file_name, "w", encoding='UTF-8') as ttl_file:
        ttl_file.write(content)


def _add_base_constructs(content, childsafe):
    pass


def _append_class(content, childsafe_item: TermDescriptor):
    content.append(f'###  {childsafe_uri_base}#{childsafe_item.name}')
    chunk = [f':{childsafe_item.name} rdf:type owl:Class']
    indent = ' '*(len(childsafe_item.name) + 2)

    for superclass in childsafe_item.superclasses:
        chunk.append(indent + f'rdfs:subClassOf :{superclass}')
    for class_name in childsafe_item.class_names:
        chunk.append(indent + f'rdf:type :{class_name}')
    if childsafe_item.label is not None:
        chunk.append(indent+f'rdfs:label "{childsafe_item.label}"@pt-BR')
    for domain in childsafe_item.domains:
        chunk.append(indent + f':definedIn "{domain}"@pt-BR')
    if childsafe_item.recommended:
        chunk.append(indent + f':isRecommendedTerm "Sim"@pt-BR')
    else:
        chunk.append(indent + f':isRecommendedTerm "Não"@pt-BR')
    for source in childsafe_item.sources:
        value = source.replace('\n', '').replace('"', "'")
        chunk.append(indent+f':sourceIs "{value}"@pt-BR')
    for link in childsafe_item.links:
        chunk.append(indent + f':linkIs "{link.strip()}"')
    if childsafe_item.comment is not None:
        value = childsafe_item.comment.replace('"', "'")
        chunk.append(indent+f'rdfs:comment """{value}"""@pt-BR')
    for equivalent in childsafe_item.equivalents:
        if equivalent.name[0] == '*':
            continue
        chunk.append(indent + f'owl:sameAs :{equivalent.name}')

    last_index = len(chunk) - 1
    for index, line in enumerate(chunk):
        content.append(line + (' ;' if index < last_index else ' .'))
    content.append('')
    content.append('')


def _append_individual(content, childsafe_item: TermDescriptor):
    chunk = [f':{childsafe_item.name} rdf:type owl:namedIndividual']
    indent = ' '*(len(childsafe_item.name) + 2)

    chunk.append(indent + f'rdf:type :{childsafe_item.name}')
    if childsafe_item.label is not None:
        chunk.append(indent+f'rdfs:label "{childsafe_item.label}"@pt-BR')
    for rel, obj in childsafe_item.relationships:
        chunk.append(indent + f':{rel} :{obj}')
    last_index = len(chunk) - 1
    for index, line in enumerate(chunk):
        content.append(line + (' ;' if index < last_index else ' .'))
    content.append('')
    content.append('')

