from core_django_app.services.services import VisualizeService


class SimpleVisualization(VisualizeService):

    def plugin_id(self):
        return "SimpleVisualization"

    def name(self):
        return "SimpleVisualization"

    def visualize(self):
        return ""



