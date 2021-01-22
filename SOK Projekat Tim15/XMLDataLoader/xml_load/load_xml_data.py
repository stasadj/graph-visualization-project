from core_django_app.models import Graph
from core_django_app.services.services import LoadDataService

import xml.etree.ElementTree as ET


class LoadXMLData(LoadDataService):
    """ Klasa koja omogucava parsiranje proizvoljnog ili specificiranog XML
    dokumenta u strukturu grafa """

    def __init__(self):
        super().__init__()
        self.graph = None

    def name(self):
        return 'LoadXMLData'

    def plugin_id(self):
        return 'XMLDataLoader'

    def load_data(self, path) -> Graph:
        """ Ucitava XML dokument sa zadate putanje

         U zavisnosti od formata zadate XML datoteke vraca graf sa ciklicnom strukturom
        ili klasicnom XML strukturom """

        xml_dom = ET.parse(path)
        attr_ref = xml_dom.find('.//*[@ref]')

        if attr_ref is None:
            self.xml_tree(xml_dom)

        else:
            self.circular_graph(xml_dom)

        return self.graph

    def circular_graph(self, xml_dom):
        """ Parsira prosledjeni XML DOM u ciklican graf """

        self.graph = Graph(True)
        root = xml_dom.getroot()

        for child in root:
            tag = child.tag
            text = child.text
            attrs = child.attrib
            attrs['elemText'] = text.strip()
            self.graph.insert_vertex(tag, attrs)

        for v1 in self.graph.vertices():
            references = v1.attributes()['ref'].split(',')
            for ref in references:
                for v2 in self.graph.vertices():
                    if ref.strip() == v2.attributes()['id']:
                        self.graph.insert_edge(v1, v2)

    def xml_tree(self, xml_dom):
        """ Parsira prosledjeni XML DOM u graf sa klasicnom XML strukturom """

        self.graph = Graph()
        element_vertex = {}

        for element in xml_dom.getiterator():
            tag = element.tag
            text = element.text
            attrs = element.attrib
            attrs['elemText'] = text.strip()
            element_vertex[element] = self.graph.insert_vertex(tag, attrs)

        for element, vertex in element_vertex.items():
            for child in element:
                self.graph.insert_edge(vertex, element_vertex[child])


