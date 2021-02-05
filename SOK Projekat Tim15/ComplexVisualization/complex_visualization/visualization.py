from core_django_app.services.services import VisualizeService
import pkg_resources


class ComplexVisualization(VisualizeService):

    def plugin_id(self):
        return "ComplexVisualization"

    def name(self):
        return "ComplexVisualization"

    def visualize(self, graph):
        pom = "var nodes_data = " + graph['nodes_data'] + ";\n"
        pom += "var links_data = " + graph['links_data'] + ";\n"
        pom += str(pkg_resources.resource_string(__name__, "visualize_graph.js"), "UTF-8")
        return pom
