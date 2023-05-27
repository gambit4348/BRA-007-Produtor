from collections import namedtuple

ChildSafeTerm = namedtuple('ChildSafeTerm',
                           ['descritor', 'relacionamentos', 'termos_relacionados', 'termos_gerais', 'classe',
                            'termos_equivalentes', 'descritivo', 'eixos', 'recomendado', 'fontes',
                            'links', 'criador', 'revisores', 'revisor_textual'])

domain_names = {
    'CA': 'Criança e Adolescente',
    'DI': 'Direito',
    'GE': 'Geral',
    'SA': 'Saúde',
    'TE': 'Tecnologia',
}


def as_id(text: str):
    return text.title().replace(' ', '_').replace('/', '_').replace('.', '')


ChildSafeRelationship = namedtuple('ChildSafeRelationship',
                                   ['name', 'object'])


class RelationshipDescriptor:
    def __init__(self, name, reverse_name=None, domain_class_name=None, range_class_name=None):
        self.name = name
        self.reverse_name = reverse_name
        self.domain_class_name = domain_class_name
        self.range_class_name = range_class_name


relationship_descriptors = {
    'aplicado em': RelationshipDescriptor('aplicadoEm', None),
    'atua em': RelationshipDescriptor('atuaEm', None),
    'assiste': RelationshipDescriptor('assiste', None, '_Agente', '_Sujeito'),
    'caracteriza': RelationshipDescriptor('caracteriza', 'caracterizadoPor'),
    'caracterizado por': RelationshipDescriptor('caracterizadoPor', 'caracteriza'),
    'causa': RelationshipDescriptor('causa', 'causadoPor', '_Causa', '_Efeito'),
    'causado por': RelationshipDescriptor('causadoPor', 'causa', '_Efeito', '_Causa'),
    'componente de': RelationshipDescriptor('componenteDe', 'compostoPor', '_Elemento', '_Todo'),
    'composto por': RelationshipDescriptor('compostoPor', 'componenteDe', '_Todo', '_Elemento'),
    'confirma': RelationshipDescriptor('confirma', 'confirmadoPor'),
    'confirmado por': RelationshipDescriptor('confirmadoPor', 'confirma'),
    'consome': RelationshipDescriptor('consome', 'consumidoPor', '_Consumidor', '_Consumível'),
    'consumido por': RelationshipDescriptor('consumidoPor', 'consome', '_Consumível', '_Consumidor'),
    'definido por': RelationshipDescriptor('definidoPor', None, '_Conceito', '_Compêndio'),
    'estimula': RelationshipDescriptor('estimula', None, '_Causa', '_Efeito'),
    'evita': RelationshipDescriptor('evita', 'evitadoPor', '_Causa', '_Efeito'),
    'evitado por': RelationshipDescriptor('evitadoPor', 'evita', '_Efeito', '_Causa'),
    'facilita': RelationshipDescriptor('facilita', 'facilitadoPor'),
    'facilitado por': RelationshipDescriptor('facilitadoPor', 'facilita'),
    'gera': RelationshipDescriptor('gera', 'geradoPor', '_Causa', '_Efeito'),
    'gerado por': RelationshipDescriptor('geradoPor', 'gera', '_Efeito', '_Causa'),
    'gerencia': RelationshipDescriptor('gerencia', 'gerenciadoPor', '_Agente', '_Organização'),
    'gerenciado por': RelationshipDescriptor('gerenciadoPor', 'gerencia', '_Organização', '_Agente'),
    'inclui': RelationshipDescriptor('inclui', None, '_Todo', '_Elemento'),
    'modifica': RelationshipDescriptor('modifica', 'modificadoPor', '_Causa', '_Sujeito'),
    'modificado por': RelationshipDescriptor('modificadoPor', 'modifica', '_Sujeito', '_Causa'),
    'ocorre durante': RelationshipDescriptor('ocorreDurante', None, '_Condição', '_Período'),
    'ocorre em': RelationshipDescriptor('ocorreEm', None, None, '_Sujeito'),
    'pode causar': RelationshipDescriptor('podeCausar', None, '_Causa', '_Condição'),
    'pode comprometer': RelationshipDescriptor('podeComprometer', None, '_Causa', '_Sujeito'),
    'pode conter': RelationshipDescriptor('podeConter', None, '_Causa', '_Condição'),
    'pode gerar': RelationshipDescriptor('podeGerar', None, '_Causa', '_Condição'),
    'pode ser': RelationshipDescriptor('podeSer', None, '_Causa', '_Condição'),
    'pode sofrer': RelationshipDescriptor('podeSofrer', None, '_Sujeito', '_Efeito'),
    'pode sofrer de': RelationshipDescriptor('podeSofrerDe', None, '_Causa', '_Condição'),
    'pratica': RelationshipDescriptor('pratica', 'praticadoPor', '_Agente', '_Processo'),
    'praticado contra': RelationshipDescriptor('praticadoContra', None, '_Processo', '_Sujeito'),
    'praticado por': RelationshipDescriptor('praticadoPor', 'pratica', '_Processo', '_Agente'),
    'provoca': RelationshipDescriptor('causa', 'causadoPor', '_Causa', '_Efeito'),
    'provocado por': RelationshipDescriptor('causadoPor', 'causa', '_Efeito', '_Causa'),
    'relativo a': RelationshipDescriptor('relativoA', None),
    'resiste a': RelationshipDescriptor('resisteA', None, '_Sujeito', '_Efeito'),
    'sofre': RelationshipDescriptor('sofre', None, '_Sujeito', '_Efeito'),
    'sofre de': RelationshipDescriptor('sofreDe', 'sofridoPor', '_Sujeito', '_Condição'),
    'sofrido por': RelationshipDescriptor('sofridoPor', 'sofreDe', '_Condição', '_Sujeito'),
    'utiliza': RelationshipDescriptor('utiliza', 'utilizadoPor', '_Usuário', '_Consumível'),
    'utilizado por': RelationshipDescriptor('utilizadoPor', 'utiliza', '_Consumível', '_Usuário'),
    'vincula': RelationshipDescriptor('vincula', 'vinculadoPor', '_Causa', '_Sujeito'),
    'vinculado por': RelationshipDescriptor('vinculadoPor', 'vincula', '_Sujeito', '_Causa'),
}


class TermDescriptor:
    def __init__(self, name: str, label: str = None, comment: str = None, recommended: bool = True, superclasses=None,
                 class_names=None, sources=None, links=None, domains=None, equivalents=None):
        self.name = name
        self.label = label
        self.comment = comment
        self.recommended = recommended
        self.superclasses = superclasses if superclasses is not None else []
        self.class_names = class_names if class_names is not None else []
        self.sources = sources if sources is not None else []
        self.links = links if links is not None else []
        self.domains = domains if domains is not None else []
        self.equivalents = equivalents if equivalents is not None else []
        self.relationships = list[RelationshipDescriptor]()

    def __repr__(self):
        return f'TermDescriptor(name={self.name}, label={self.label})'

    def __str__(self):
        return f'name={self.name}, label={self.label}'

    def append_class_name(self, term_id):
        if not self.superclass_exists(term_id):
            self.superclasses.append(term_id)

    def append_rel(self, name, class_name):
        if not self.relationship_exists(name, class_name):
            self.relationships.append(ChildSafeRelationship(name, class_name))

    def append_superclass(self, term_id):
        if not self.superclass_exists(term_id):
            self.superclasses.append(term_id)

    def class_name_exists(self, term_id):
        for class_name in self.class_names:
            if class_name == term_id:
                return True
        return False

    def relationship_exists(self, relationship: str, related_item: str):
        for rel, obj in self.relationships:
            if rel == relationship and obj == related_item:
                return True
        return False

    def superclass_exists(self, term_id):
        for superclass in self.superclasses:
            if superclass == term_id:
                return True
        return False


class ChildSafe:
    """
    Ontological representation of a Child-Safe vocabulary.
    """

    def __init__(self, vocabulary: list[dict]):
        """
        ChildSafe constructor.

        :param vocabulary: a list of dicts containing definitions of a single vocabulary term.
        """

        self.ids_terms = dict()
        # Primeiro incluímos os termos equivalentes no vocabulário para que eles possam ser
        # corretamente referenciados por seus identificadores quando os termos principais forem incluídos
        for vocabulary_item in vocabulary:
            for equivalent_term in vocabulary_item['equivalentes']:
                equivalent_term = equivalent_term.strip()
                if equivalent_term == '': # or equivalent_term[0] == '*':
                    continue
                term_label = equivalent_term.capitalize()
                term_id = as_id(term_label)
                if term_id == term_label:
                    term_label = None
                if term_id not in self.ids_terms:
                    self.ids_terms[term_id] = TermDescriptor(term_id, label=term_label)

        # Agora incluímos os termos principais já configurados com suas propriedades básicas e os equivalentes.
        # Termos relacionados e nomes de classes são deixadas para depois para garantir que todos os identificadores
        # já tenham sido criados
        for vocabulary_item in vocabulary:
            termo = vocabulary_item['termo'].strip().capitalize()
            term_label = termo
            term_id = as_id(term_label)
            if term_id == term_label:
                term_label = None
            term = TermDescriptor(name=term_id, label=term_label, comment=vocabulary_item['definicao'],
                                  recommended=vocabulary_item['recomendado'],
                                  sources=vocabulary_item['fontes'], links=vocabulary_item['links'],
                                  domains=[domain_names[eixo] for eixo in vocabulary_item['eixos']])
            self.ids_terms[term_id] = term

            for equivalent_term in vocabulary_item['equivalentes']:
                equivalent_term = equivalent_term.strip()
                if equivalent_term == '':
                    continue
                term_label = equivalent_term.capitalize()
                term_id = as_id(term_label)
                term.equivalents.append(self.ids_terms[term_id])
                self.ids_terms[term_id].equivalents.append(term)

        # Agora relacionamos superclasses e nomes de classes
        for vocabulary_item in vocabulary:
            termo = vocabulary_item['termo'].strip().capitalize()
            term_id = as_id(termo)
            if term_id not in self.ids_terms:
                print(f'Termo "{termo}" ({term_id}) NÃO encontrado.')
                continue
            term = self.ids_terms[term_id]
            for termo_geral in vocabulary_item['termos_gerais']:
                term_id = as_id(termo_geral.strip().capitalize())
                if term_id not in self.ids_terms:
                    print(f'Termo "{termo}": referência a termo geral "{termo_geral}" NÃO definido.')
                    continue
                term.append_superclass(term_id)
            for class_name in vocabulary_item['classes']:
                term_id = as_id(class_name.strip().capitalize())
                if term_id not in self.ids_terms:
                    print(f'Termo "{termo}": referência a nome de classe "{class_name}" NÃO definido.')
                    continue
                term.append_class_name(term_id)

        # Agora estabelecemos os relacionamentos entre os termos
        for vocabulary_item in vocabulary:
            termo = vocabulary_item['termo'].strip().capitalize()
            term = self.ids_terms[as_id(termo)]
            if len(vocabulary_item['relacionamentos']) > 0:
                for relationship, related_item in zip(vocabulary_item['relacionamentos'],
                                                      vocabulary_item['termos_relacionados']):
                    related_id = as_id(related_item)
                    if related_id not in self.ids_terms:
                        print(f'Termo relacionado "{related_item}" NÃO definido em "{term}".')
                        continue
                    related_item = self.ids_terms[related_id]
                    relationship = relationship.lower()
                    if relationship in relationship_descriptors:
                        relationship_descriptor = relationship_descriptors[relationship]
                        term.append_rel(relationship_descriptor.name, related_item.name)
                        if relationship_descriptor.domain_class_name is not None:
                            term.append_class_name(relationship_descriptor.domain_class_name)
                        if relationship_descriptor.range_class_name is not None:
                            related_item.append_class_name(relationship_descriptor.range_class_name)
                        if relationship_descriptor.reverse_name is not None:
                            related_item.append_rel(relationship_descriptor.reverse_name, term.name)
                    else:
                        print(
                            f'Relacionamento NÃO definido: "{relationship}" em "{termo}" com "{related_item.name}"')

        self.items = list(self.ids_terms.values())
        self.items.sort(key=lambda item: item.name.lower())

    def __str__(self):
        return f'Item count={len(self.items)}'
