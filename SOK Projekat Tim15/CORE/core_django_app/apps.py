import pkg_resources
from django.apps import AppConfig


class CoreDjangoAppConfig(AppConfig):
    name = 'core_django_app'
    verbose_name = 'CORE DJANGO APP'
    graph = None
    load_data_plugins = {}
    visualize_data_plugins = {}

    def ready(self):
        self.load_data_plugins = self.load_plugins("load.data")
        self.visualize_data_plugins = self.load_plugins("visualize.data")
        #  test
        self.graph = self.load_data_plugins['DeezerDataLoader'].load_data("https://api.deezer.com/playlist/6033056424")
        print(self.visualize_data_plugins['SimpleVisualization'].visualize())

    def load_plugins(self, oznaka):
        plugins = {}
        for ep in pkg_resources.iter_entry_points(group=oznaka):
            p = ep.load()
            #print("{} {}".format(ep.name, p))
            plugin = p()
            plugins[plugin.plugin_id()] = plugin
        return plugins
