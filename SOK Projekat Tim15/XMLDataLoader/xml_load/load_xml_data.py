from core_django_app.models import Graph
from core_django_app.services.services import LoadDataService


class LoadXMLData(LoadDataService):
    def __init__(self):
        super().__init__()

    def name(self):
        return 'LoadXMLData'

    def plugin_id(self):
        return 'XMLDataLoader'

    def load_data(self, path) -> Graph:
        pass
