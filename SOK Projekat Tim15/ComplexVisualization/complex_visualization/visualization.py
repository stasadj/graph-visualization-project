from core_django_app.services.services import VisualizeService
import pkg_resources


class ComplexVisualization(VisualizeService):

    def plugin_id(self):
        return "ComplexVisualization"

    def name(self):
        return "ComplexVisualization"

    def visualize(self):
        pom = pkg_resources.resource_string(__name__, "visualize_graph.js")
        return str(pom, "UTF-8")
