import pkg_resources
from django.apps import AppConfig


class CoreDjangoAppConfig(AppConfig):
    name = 'core_django_app'
    verbose_name = 'CORE DJANGO APP'
    graph = None
    load_data_plugins = {}
    visualize_data_plugins = {}
    chosen_load_plugin = None
    chose_visualize_plugin = None

    def ready(self):
        self.load_data_plugins = self.load_plugins("load.data")
        self.visualize_data_plugins = self.load_plugins("visualize.data")

    def load_plugins(self, entry_point):
        plugins = {}
        for ep in pkg_resources.iter_entry_points(group=entry_point):
            p = ep.load()
            #print("{} {}".format(ep.name, p))
            plugin = p()
            plugins[plugin.plugin_id()] = plugin
        return plugins
