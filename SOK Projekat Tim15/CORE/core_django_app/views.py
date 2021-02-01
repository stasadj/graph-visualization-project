from django.shortcuts import render, redirect
from django.apps.registry import apps #dina dodala

# Create your views here.
from core_django_app.models import Graph
from core_django_app.apps import CoreDjangoAppConfig


def index(request):

    config = apps.get_app_config('core_django_app')
    title = config.verbose_name

    load_plugins = config.load_data_plugins
    visualize_plugins = config.visualize_data_plugins
    return render(request, "index.html", {"title": title,
                                          "load_plugins":  load_plugins,
                                          "visualize_plugins": visualize_plugins})


def visualize_data(request):

    if request.method == 'POST':

        config = apps.get_app_config('core_django_app')
        load_plugins = config.load_data_plugins
        visualize_plugins = config.visualize_data_plugins

        if config.graph is None:
            return render(request, "index.html", {"title": config.verbose_name,
                                                      "data_not_loaded": True,
                                                      "load_plugins": load_plugins,
                                                      "visualize_plugins": visualize_plugins})


        #TODO: Spojiti ova dva naredna ifa
        if request.POST.get('visualization_plugin') == 'SimpleVisualization':
            plugin = config.visualize_data_plugins['SimpleVisualization']
            config.chosen_visualize_plugin = plugin
            return render(request, "index.html", {"title": "Main View",
                                                    "plugin": plugin,
                                                    "data_visualized": True,
                                                    "graph": config.graph,
                                                    "load_plugins": load_plugins,
                                                    "visualize_plugins": visualize_plugins})

        if request.POST.get('visualization_plugin') == 'ComplexVisualization':
            plugin = config.visualize_data_plugins['ComplexVisualization']
            config.chosen_visualize_plugin = plugin
            return render(request, "index.html", {"title": "Main View",
                                                      "plugin": plugin,
                                                      "data_visualized": True,
                                                      "graph": config.graph,
                                                      "load_plugins": load_plugins,
                                                      "visualize_plugins": visualize_plugins})

    else:
        return redirect('index')


def load_data(request):

    if request.method == 'POST':

        config = apps.get_app_config('core_django_app')
        load_plugins = config.load_data_plugins
        visualize_plugins = config.visualize_data_plugins

        if request.POST.get('source_plugin') == 'XMLDataLoader':
            try:
                xml_file = request.FILES['xml_file'].read()
            except KeyError:
                return render(request, "index.html", {"title": config.verbose_name,
                                                      "data_not_loaded": True,
                                                      "load_plugins": load_plugins,
                                                      "visualize_plugins": visualize_plugins})

            xml_file_utf8 = str(xml_file, 'UTF-8')
            plugin = config.load_data_plugins['XMLDataLoader']
            config.graph = plugin.load_data(xml_file_utf8)
            config.chosen_load_plugin = plugin
            return render(request, "index.html", {"title": "Data Loaded",
                                                      "data_loaded": True,
                                                      "graph": config.graph,
                                                      "load_plugins": load_plugins,
                                                      "visualize_plugins": visualize_plugins})

        if request.POST.get('source_plugin') == 'DeezerDataLoader':
            playlist_path = request.POST.get('playlist_link')

            if playlist_path is None or playlist_path == '':
                return render(request, "index.html", {"title": config.verbose_name,
                                                      "data_not_loaded": True,
                                                      "load_plugins": load_plugins,
                                                      "visualize_plugins": visualize_plugins})

            plugin = config.load_data_plugins['DeezerDataLoader']
            config.graph = plugin.load_data(playlist_path)
            return render(request, "index.html", {"title": "Data Loaded",
                                                  "data_loaded": True,
                                                  "graph": config.graph,
                                                  "load_plugins": load_plugins,
                                                  "visualize_plugins": visualize_plugins})

    else:
        return redirect('index')


def search_data(request):

    config = apps.get_app_config('core_django_app')
    if config.chosen_visualize_plugin is None:
        return redirect("index")

    parameter = request.POST["search_input"]

    new_graph = create_search_graph(parameter)

    return render(request, "index.html", {"title": "Main View",
                                              "plugin": config.chosen_visualize_plugin,
                                              "graph": new_graph,
                                              "data_visualized": True,
                                              "load_plugins": config.load_data_plugins,
                                              "visualize_plugins": config.visualize_data_plugins})


def create_search_graph(parameter):
    config = apps.get_app_config('core_django_app')
    old_graph = config.graph
    new_graph = Graph(old_graph.is_directed())

    for v in old_graph.vertices():
        if parameter.lower() in v.name().lower() or parameter.lower() in v.element_type().lower():
            new_graph.insert_vertex_object(v)
        else:
            for val in v.attributes().values():
                if parameter.lower() in val.lower():
                    print(val.lower())
                    new_graph.insert_vertex_object(v)

    for v in new_graph.vertices():
        for v2 in new_graph.vertices():
            if v is not v2:
                if old_graph.get_edge(v, v2) is not None and new_graph.get_edge(v, v2) is None:
                    new_graph.insert_edge(v, v2) #todo ili da dodas postojeci objekat?

    return new_graph


def filter_data(request):
    #TODO: filter

    return redirect("index")
