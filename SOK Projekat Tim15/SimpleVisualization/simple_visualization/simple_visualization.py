from core_django_app.services.services import VisualizeService
import pkg_resources

class SimpleVisualization(VisualizeService):

    def plugin_id(self):
        return "SimpleVisualization"

    def name(self):
        return "SimpleVisualization"

    def visualize(self):
        f = open("simple_visualize_graph.js", "r")
        str = f.read()
        f.close()
        return str
