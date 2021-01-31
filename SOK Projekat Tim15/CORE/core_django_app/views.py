from django.shortcuts import render, redirect
from django.apps.registry import apps #dina dodala

# Create your views here.


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

        if request.POST.get('visualization_plugin') == 'SimpleVisualization':
            plugin = config.visualize_data_plugins['SimpleVisualization']
            return render(request, "main_view.html", {"title": "Main View",
                                                    "plugin": plugin,
                                                    "graph": config.graph,
                                                    "load_plugins": load_plugins,
                                                    "visualize_plugins": visualize_plugins})

        if request.POST.get('visualization_plugin') == 'ComplexVisualization':
            # TODO: ComplexVisualization
            return redirect('index')

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