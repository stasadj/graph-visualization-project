from core_django_app.services.services import VisualizeService
import pkg_resources


class SimpleVisualization(VisualizeService):

    def plugin_id(self):
        return "SimpleVisualization"

    def name(self):
        return "SimpleVisualization"

    def visualize(self, graph):
        pom = "var nodes_data = " + graph['nodes_data'] + ";\n"
        pom += "var links_data = " + graph['links_data'] + ";\n"
        pom += str(pkg_resources.resource_string(__name__, "simple_visualize_graph.js"), "UTF-8")
        return pom
