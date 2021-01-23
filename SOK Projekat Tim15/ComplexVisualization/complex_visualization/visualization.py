from core_django_app.services.services import VisualizeService

class ComplexVisualization(VisualizeService):
    # Dummy class, TODO change this class and its methods
    def __init__(self):
        super().__init__()
        self.graph_visualization = None

    def add_graph(self,graph):
        self.graph_visualization = graph

    def visualize(self):
        # povratna vrednost js kod
        pass