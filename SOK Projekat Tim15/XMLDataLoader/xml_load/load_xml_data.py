from core_django_app.models import Graph
from core_django_app.services.services import LoadDataService

import xml.etree.ElementTree as ET


class LoadXMLData(LoadDataService):
    """ Klasa koja omogucava parsiranje proizvoljnog ili specificiranog XML
    dokumenta u strukturu grafa

    Specificirani XML dokument se prepoznaje na osnovu postojanja 'ref' i 'id' atributa unutar elemenata

    'ref' atribut je oblika 'ref' = 'id', 'id', 'id'..."""

    def __init__(self):
        super().__init__()
        self.graph = None

    def name(self):
        return 'LoadXMLData'

    def plugin_id(self):
        return 'XMLDataLoader'

    def load_data(self, path) -> Graph:
        """ Parsira prosledjeni XML string

         U zavisnosti od formata zadate XML datoteke vraca graf sa ciklicnom strukturom
        ili klasicnom XML strukturom """

        xml_dom = ET.ElementTree(ET.fromstring(path))
        attr_ref = xml_dom.find('.//*[@ref]')

        if attr_ref is None:
            self.xml_tree(xml_dom)

        else:
            self.circular_graph(xml_dom)

        return self.graph

    def circular_graph(self, xml_dom):
        """ Parsira prosledjeni XML DOM u ciklican graf """

        self.graph = Graph()
        element_vertex = self.create_element_vertex_dict(xml_dom)

        for element, vertex in element_vertex.items():
            for child in element:
                self.graph.insert_edge(vertex, element_vertex[child])

            if 'ref' in element.attrib:
                references = element.attrib['ref'].split(',')
                for ref in references:
                    for elem in element_vertex.keys():
                        if 'id' in elem.attrib and elem.attrib['id'] == ref.strip():
                            self.graph.insert_edge(vertex, element_vertex[elem])

    def xml_tree(self, xml_dom):
        """ Parsira prosledjeni XML DOM u stablo sa klasicnom XML strukturom """

        self.graph = Graph()
        element_vertex = self.create_element_vertex_dict(xml_dom)

        for element, vertex in element_vertex.items():
            for child in element:
                self.graph.insert_edge(vertex, element_vertex[child])

    def create_element_vertex_dict(self, xml_dom):
        """ Vraca recnik u kome su kljucevi XML DOM elementi a vrednosti njihovi odgovarajuci cvorovi u grafu """

        element_vertex = {}

        if self.graph is None:
            return element_vertex

        for element in xml_dom.getiterator():
            tag = element.tag
            attrs = element.attrib
            if element.text is not None:
                text = element.text.strip()
            else:
                text = ''
            element_vertex[element] = self.graph.insert_vertex(tag, attrs, text)

        return element_vertex
