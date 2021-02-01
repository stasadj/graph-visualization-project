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
            return render(request, "main_view.html", {"title": "Main View",
                                                    "plugin": plugin,
                                                    "data_visualized": True,
                                                    "graph": config.graph,
                                                    "load_plugins": load_plugins,
                                                    "visualize_plugins": visualize_plugins})

        if request.POST.get('visualization_plugin') == 'ComplexVisualization':
            plugin = config.visualize_data_plugins['ComplexVisualization']
            config.chosen_visualize_plugin = plugin
            return render(request, "main_view.html", {"title": "Main View",
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

    return render(request, "main_view.html", {"title": "Main View",
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


def value_passes_query(vertex_value, query_operator, query_value):

    if query_operator == "==":
        return vertex_value == query_value

    elif query_operator == "!=":
        return vertex_value != query_value

    elif query_operator == ">":
        return vertex_value > query_value

    elif query_operator == "<":
        return vertex_value < query_value

    elif query_operator == ">=":
        return vertex_value >= query_value

    elif query_operator == "<=":
        return vertex_value <= query_value


def create_filter_graph(query_tokens):
    config = apps.get_app_config('core_django_app')
    old_graph = config.graph
    new_graph = Graph(old_graph.is_directed())

    query_attribute = query_tokens[0]
    query_operator = query_tokens[1]
    query_value = query_tokens[2]

    for v in old_graph.vertices():
        # Checking if vertex attributes contain attribute in query
        if query_attribute in v.attributes().keys():
            if value_passes_query(v.attributes()[query_attribute], query_operator, query_value):
                new_graph.insert_vertex_object(v)

    # Checking if there are any edges between the chosen vertices
    for v in new_graph.vertices():
        for v2 in new_graph.vertices():
            if v is not v2:
                if old_graph.get_edge(v, v2) is not None and new_graph.get_edge(v, v2) is None:
                    new_graph.insert_edge(v, v2)  # todo ili da dodas postojeci objekat?

    return new_graph


def query_format_correct(query):
    tokens = query.split(" ")
    if len(tokens) < 3:
        return False
    if tokens[1] not in ["==", "!=", ">", "<", "<=", ">="]:
        return False
    return True


def get_query_tokens(query):
    parts = query.split(" ")
    return [parts[0], parts[1], " ".join(parts[2:])]


def filter_data(request):
    config = apps.get_app_config('core_django_app')
    
    # Preventing filtering if no data is displayed
    if config.chosen_visualize_plugin is None:
        return redirect("index")

    query = request.POST["filter_input"]
    if not query_format_correct(query):
        # if the query format isn't correct, we show the original graph again with an error message
        return render(request, "main_view.html", {"title": "Main View",
                                                  "plugin": config.chosen_visualize_plugin,
                                                  "graph": config.graph,
                                                  "data_visualized": True,
                                                  "error_message": "Incorrect filter query format!",
                                                  "load_plugins": config.load_data_plugins,
                                                  "visualize_plugins": config.visualize_data_plugins})
    
    new_graph = create_filter_graph(get_query_tokens(query))
    return render(request, "main_view.html", {"title": "Main View",
                                              "plugin": config.chosen_visualize_plugin,
                                              "graph": new_graph,
                                              "data_visualized": True,
                                              "load_plugins": config.load_data_plugins,
                                              "visualize_plugins": config.visualize_data_plugins})
