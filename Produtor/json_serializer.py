import json
import re
import unicodedata
from spacy.lang.pt import Portuguese
from childsafe import ChildSafe, TermDescriptor


nlp = Portuguese()


class WordNode:
    def __init__(self, term):
        self.term = term
        self.words = dict()

    def next(self, word):
        if word in self.words:
            return self.words[word]
        return None


class Automaton:
    def __init__(self):
        self.words = dict()

    def add(self, term):
        label = term.label if term.label is not None else term.name
        words = label.casefold().split()
        self._add_term(term, words)
        for equivalent_term in term.equivalents:
            equivalent_label = equivalent_term.label if equivalent_term.label is not None else equivalent_term.name
            if equivalent_label != '' and equivalent_label[0] == '*':
                equivalent_label = equivalent_label[1:]
            words = equivalent_label.casefold().split()
            self._add_term(term, words)

    def _add_term(self, term, words):
        current_node = None
        next_node = None
        for word in words:
            if current_node is None:
                next_node = self.start(word)
            else:
                next_node = current_node.next(word)
            if next_node is None:
                next_node = WordNode(term if word == words[-1] else None)
                if current_node is None:
                    self.words[word] = next_node
                else:
                    current_node.words[word] = next_node
                current_node = next_node
            elif word == words[-1]:
                if current_node is not None:
                    current_node.term = term
            else:
                current_node = next_node

    def start(self, word: str) -> WordNode:
        if word in self.words:
            return self.words[word]
        return None


def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)


def text_to_id(text):
    """
    Convert input text to id.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    text = strip_accents(text.lower())
    text = re.sub('[ ]+', '_', text)
    text = re.sub('[^0-9a-zA-Z_-]', '', text)
    return text


def as_json(vocabulario):
    vocabulario_json = json.dumps(vocabulario, indent=2)
    return vocabulario_json


def as_json_name(name: str) -> str:
    return text_to_id(name)


names_terms = dict()


def export_to_json(child_safe: ChildSafe, file_name):
    items = [item for item in child_safe.items if item.comment is not None]
    _index_terms(items)

    automaton = Automaton()
    added = set()
    for term in items:
        automaton.add(term)

    domain_tags = {
        'Criança e Adolescente': 'CA',
        'Direito': 'DI',
        'Geral': 'GE',
        'Saúde': 'SA',
        'Tecnologia': 'TE'
    }

    def term_name(term: TermDescriptor):
        return term.label if term.label is not None else term.name

    def exportable_equivalents(equivalents: list[TermDescriptor]):
        terms = [term_name(term) for term in equivalents if term_name(term)[0] != '*']
        return list(set(terms))

    json_items = [{
        'nome': as_json_name(item.name),
        'descritor': item.label if item.label is not None else item.name,
        'definicao': hyperlinked_text(item, automaton),
        'equivalentes': exportable_equivalents(item.equivalents),
        'eixos': [domain_tags[domain] for domain in item.domains],
        'recomendado': item.recommended,
        'fontes': item.sources,
        'links': item.links,
    } for item in child_safe.items]

    json_file_header = '// Vocabulário semântico do projeto BRA/01/007 - Observatório Nacional para a Prevenção de '\
                       'Crimes contra a Criança e o Adolescente\n'
    json_content = f'{json_file_header}\n\nvar vocabulario = {as_json(json_items)};\n'

    file_path = file_name
    with open(file_path, 'w') as json_file:
        json_file.write(json_content)
    print(f'\nGravado o arquivo {file_path}')


def space_before(token):
    return token != ',' and token != '.' and token != ';' and token != ')'


def hyperlinked_text(term, automaton):
    text = ''
    doc = nlp(term.comment) if term.comment is not None else None
    tokens = [token.text for token in doc] if doc is not None else []
    original_term_name = term.label.casefold() if term.label is not None else term.name.casefold()

    node_parts = []
    name_parts = []
    current_node = None
    for token in tokens:
        if current_node is None:
            next_node = automaton.start(token)
        else:
            next_node = current_node.next(token)
        if next_node is None:
            if len(node_parts) > 0:
                complete_name = ' '.join(name_parts)
                target_term = names_terms[complete_name] if complete_name in names_terms else None
                if target_term is not None:
                    term_name = target_term.label.casefold() if target_term.label is not None \
                                                             else target_term.name.casefold()
                    json_name = as_json_name(term_name)
                else:
                    json_name = None
                if json_name is not None and complete_name != original_term_name and node_parts[-1].term is not None:
                    link = f' <a href="#{json_name}">' + complete_name + '</a>'
                    text += link
                else:
                    text += ' ' + complete_name
                next_node = automaton.start(token)
                if next_node is not None:
                    node_parts = [next_node]
                    name_parts = [token]
                else:
                    node_parts = []
                    name_parts = []
            if next_node is None:
                text += (' ' if space_before(token) else '') + token
        else:
            node_parts.append(next_node)
            name_parts.append(token)
        current_node = next_node
    return text.strip()


def _index_terms(terms: list[TermDescriptor]):
    for term in terms:
        name = term.label.casefold() if term.label is not None else term.name.casefold()
        names_terms[name] = term
        for equivalent_term in term.equivalents:
            equivalent_name = equivalent_term.label.casefold() if equivalent_term.label is not None \
                                                               else equivalent_term.name.casefold()
            if equivalent_name != '' and equivalent_name[0] == '*':
                equivalent_name = equivalent_name[1:]
            names_terms[equivalent_name] = term

