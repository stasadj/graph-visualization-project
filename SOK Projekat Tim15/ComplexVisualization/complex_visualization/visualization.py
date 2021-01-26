from core_django_app.services.services import VisualizeService
import pkg_resources

class ComplexVisualization(VisualizeService):
    # Dummy class, TODO change this class and its methods
    def __init__(self):
        super().__init__()
        self.graph = None

    def add_graph(self,graph):
        self.graph = graph

    def visualize(self):
        pom = pkg_resources.resource_string(__name__, "visualize_graph.js")
        return str(pom, "UTF-8")