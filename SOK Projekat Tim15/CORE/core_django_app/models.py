import json
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
# -*- coding: utf-8 -*-



class Graph:
    """ Reprezentacija jednostavnog grafa"""

    # ------------------------- Ugnježdena klasa Vertex -------------------------
    class Vertex:
        """ Struktura koja predstavlja čvor grafa."""
        __slots__ = '_element_type', '_attributes', '_id', '_name'

        def __init__(self, el_type, attrs, idv, name):
            self._element_type = el_type #element_type in our case is either Track/Playlist/Artist or some XML tag
            self._attributes = attrs #dictionary od Vertex attributes (in our case for Track: albumcover, duration.. or xml attributes)
            self._id = idv #unique vertex id - int
            self._name = name #vertex name - in our case Track Name or text between xml tags

        def element_type(self):
            """Vraća element vezan za čvor grafa."""
            return self._element_type

        def attributes(self):
            return self._attributes

        def id(self):
            return self._id

        def name(self):
            return self._name

        def __hash__(self):  # omogućava da Vertex bude ključ mape
            return hash(id(self))

        def __str__(self):
            return str(self._element_type) + ": " + str(self._name)

        def get_json_attributes(self):
            return json.dumps(self.attributes())

    # ------------------------- Ugnježdena klasa Edge -------------------------
    class Edge:
        """ Struktura koja predstavlja ivicu grafa """
        __slots__ = '_origin', '_destination', '_element', '_id'

        def __init__(self, origin, destination, element, idv):
            self._origin = origin
            self._destination = destination
            self._element = element
            self._id = idv

        def endpoints(self):
            """ Vraća torku (u,v) za čvorove u i v."""
            return self._origin, self._destination

        def opposite(self, v):
            """ Vraća čvor koji se nalazi sa druge strane čvora v ove ivice."""
            if not isinstance(v, Graph.Vertex):
                raise TypeError('v mora biti instanca klase Vertex')

            return self._destination if v is self._origin else self._origin
            # raise ValueError('v nije čvor ivice')  unreachable

        def element(self):
            """ Vraća element vezan za ivicu"""
            return self._element

        def __hash__(self):  # omogućava da Edge bude ključ mape
            return hash((self._origin, self._destination))

        def __str__(self):
            return '({0},{1},{2})'.format(self._origin, self._destination, self._element)

    # ------------------------- Metode klase Graph -------------------------
    def __init__(self, directed=True):
        """ Kreira prazan graf (podrazumevana vrednost je da je neusmeren).

        Ukoliko se opcioni parametar directed postavi na True, kreira se usmereni graf.
        """
        self._outgoing = {}
        # ukoliko je graf usmeren, kreira se pomoćna mapa
        self._incoming = {} if directed else self._outgoing

    def _validate_vertex(self, v):
        """ Proverava da li je v čvor(Vertex) ovog grafa."""
        if not isinstance(v, self.Vertex):
            raise TypeError('Očekivan je objekat klase Vertex')

        if v not in self._outgoing:
            raise ValueError('Vertex ne pripada ovom grafu.')

    def is_directed(self):
        """ Vraća True ako je graf usmeren; False ako je neusmeren."""
        return self._incoming is not self._outgoing  # graf je usmeren ako se mape razlikuju

    def vertex_count(self):
        """ Vraća broj čvorova u grafu."""
        return len(self._outgoing)

    def vertices(self):
        """ Vraća iterator nad svim čvorovima grafa."""
        return self._outgoing.keys()

    def edge_count(self):
        """ Vraća broj ivica u grafu."""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # ukoliko je graf neusmeren, vodimo računa da ne brojimo čvorove više puta
        return total if self.is_directed() else total // 2

    def edges(self):
        """ Vraća set svih ivica u grafu."""
        result = set()  # pomoću seta osiguravamo da čvorove neusmerenog grafa brojimo samo jednom
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())  # dodavanje ivice u rezultujući set
        return result

    def get_edge(self, u, v):
        """ Vraća ivicu između čvorova u i v ili None ako nisu susedni."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        """ Vraća stepen čvora - broj(odlaznih) ivica iz čvora v u grafu.

        Ako je graf usmeren, opcioni parametar outgoing se koristi za brojanje dolaznih ivica.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """ Vraća sve (odlazne) ivice iz čvora v u grafu.

        Ako je graf usmeren, opcioni parametar outgoing se koristi za brojanje dolaznih ivica.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None, attrs=None, name=None):
        """ Ubacuje i vraća novi čvor (Vertex) sa elementom x"""
        v = self.Vertex(x, attrs, self.vertex_count()+1, name)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}  # mapa različitih vrednosti za dolazne čvorove
        return v

    def insert_vertex_object(self, v):
        """ Ubacuje i vraća novi čvor (Vertex) sa elementom x"""
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}  # mapa različitih vrednosti za dolazne čvorove
        return v

    def insert_edge(self, u, v, x=None):
        """ Ubacuje i vraća novu ivicu (Edge) od u do v sa pomoćnim elementom x.

        Baca ValueError ako u i v nisu čvorovi grafa.
        Baca ValueError ako su u i v već povezani.
        """
        if self.get_edge(u, v) is not None:  # uključuje i proveru greške
            raise ValueError('u and v are already adjacent')
        e = self.Edge(u, v, x, self.edge_count()+1)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e

    def is_isolated(self, v):
        if len(self._incoming[v]) == 0 and len(self._outgoing[v]) == 0:
            return True
        else:
            return False

    def is_hanging(self, v):
        if len(self._incoming[v]) == 0:
            return True
        else:
            return False

    def has_hanging(self):
        for v in self.vertices():
            if len(self._incoming[v]) == 0:
                return True
        return False

    def is_connected(self):
        for v in self.vertices():
            if self.is_isolated(v):
                return False
        return True

    def roots(self):
        roots = []
        vertex_degree = {}
        vertices = self.vertices()
        has_hanging = self.has_hanging()

        for v in vertices:
            if has_hanging:
                if self.is_hanging(v):
                    roots.append(v)
            else:
                vertex_degree[v] = self.degree(v)

        if len(vertex_degree) > 0:
            max_key = max(vertex_degree, key=lambda k: vertex_degree[k])
            roots.append(max_key)

        return roots

    def get_json_graph(self):
        ''' Vraca python recnik sa kljucevima nodes_data i links_data cije su vrednosti odgovarajuci json stringovi '''

        graph = {}
        graph['nodes_data'] = []
        graph['links_data'] = []

        for v in self.vertices():
            graph['nodes_data'].append({'id': v.id(), 'name': v.name(), 'element_type': v.element_type(), 'atributes': v.attributes()})

        for e in self.edges():
            graph['links_data'].append({'source': e.endpoints()[0].id(), 'target': e.endpoints()[1].id()})

        graph['nodes_data'] = json.dumps(graph['nodes_data'])
        graph['links_data'] = json.dumps(graph['links_data'])
        return graph


    # Search methods: --------------------------------------------------------------------------------------------------

    def create_search_graph(self, parameter):
        """
        Method creates a subgraph based on the search keyword
        :param parameter: search keyword
        :return: Graph object which is a subgraph containing the nodes and edges which fit the keyword
        """
        new_graph = Graph(self.is_directed())

        try_float = ignore_exception(ValueError)(float)
        try_int = ignore_exception(ValueError)(int)

        for v in self.vertices():
            # Element_type check
            # The element_type of a vertex is always a string
            if parameter.lower() in v.element_type().lower():
                new_graph.insert_vertex_object(v)
                continue

            # Name check
            # First we try to convert the parameter to the type of the vertex' name
            converted_parameter = ignore_exception(ValueError)(type(v.name()))(parameter)

            # If it's not None, that means the conversion was successful and we can go on and compare the values
            if converted_parameter is not None:
                if type(v.name()) == str:
                    if converted_parameter.lower() in v.name().lower():
                        new_graph.insert_vertex_object(v)
                        continue
                else:
                    if v.name() == converted_parameter:
                        new_graph.insert_vertex_object(v)
                        continue

            # Attributes
            # Same as for Name for each attribute
            for val in v.attributes().values():
                converted_parameter = ignore_exception(ValueError)(type(val))(parameter)
                if converted_parameter is not None:
                    if type(val) == str:
                        if converted_parameter.lower() in val.lower():
                            new_graph.insert_vertex_object(v)
                            break  # if attribute match, we don't look at the rest to prevent duplicate vertices
                    else:
                        if val == converted_parameter:
                            new_graph.insert_vertex_object(v)
                            break  # if attribute match, we don't look at the rest to prevent duplicate vertices


        # Checking if there are any edges between the chosen vertices
        for v in new_graph.vertices():
            for v2 in new_graph.vertices():
                if v is not v2:
                    if self.get_edge(v, v2) is not None and new_graph.get_edge(v, v2) is None:
                        new_graph.insert_edge(v, v2)  # todo ili da dodas postojeci objekat?

        return new_graph


    # Filter methods: --------------------------------------------------------------------------------------------------

    def create_filter_graph(self, query_tokens):
        """
        Method creates a subgraph based on the filter query
        :param query_tokens: list of words of the query, for example: ["name", "==", "Bohemian rapsody"]
        :return: Graph object which is a subgraph containing the nodes and edges which fit the filter query
        """
        new_graph = Graph(self.is_directed())

        query_attribute = query_tokens[0]
        query_operator = query_tokens[1]
        query_value = query_tokens[2]

        for v in self.vertices():

            # if query matches: "<element_type> <operator> <name>"
            # then we can try and convert the value to the type of vertex' name
            # and compare them
            converted_query_value = ignore_exception(ValueError)(type(v.name()))(query_value)
            if query_attribute.lower() == v.element_type().lower() and converted_query_value is not None:
                if value_passes_query(v.name(), query_operator, converted_query_value):
                    new_graph.insert_vertex_object(v)
                    continue


            # Checking if attributes contain attribute and value from query
            if query_attribute in v.attributes().keys():
                converted_query_value = ignore_exception(ValueError)(type(v.attributes()[query_attribute]))(query_value)
                if converted_query_value is not None:
                    if value_passes_query(v.attributes()[query_attribute], query_operator, converted_query_value):
                        new_graph.insert_vertex_object(v)



        # Checking if there are any edges between the chosen vertices
        for v in new_graph.vertices():
            for v2 in new_graph.vertices():
                if v is not v2:
                    if self.get_edge(v, v2) is not None and new_graph.get_edge(v, v2) is None:
                        new_graph.insert_edge(v, v2)  # todo ili da dodas postojeci objekat?

        return new_graph



def value_passes_query(vertex_value, query_operator, query_value):
    if query_operator == "==":
        return vertex_value == query_value

    elif query_operator == "!=":
        return vertex_value != query_value

    elif query_operator == ">":
        return vertex_value > query_value

    elif query_operator == "<":
        return vertex_value < query_value

    elif query_operator == ">=":
        return vertex_value >= query_value

    elif query_operator == "<=":
        return vertex_value <= query_value


def ignore_exception(IgnoreException=Exception, DefaultVal=None):
    """ Decorator for ignoring exception from a function
    e.g.   @ignore_exception(DivideByZero)
    e.g.2. ignore_exception(DivideByZero)(Divide)(2/0)
    """
    def dec(function):
        def _dec(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IgnoreException:
                return DefaultVal
        return _dec
    return dec