from django.shortcuts import render, redirect
from django.apps.registry import apps #dina dodala

# Create your views here.


def index(request):

    config = apps.get_app_config('core_django_app')
    title = config.verbose_name

    plagini_ucitavanje = config.load_data_plugins
    plagini_vizualizacija = config.visualize_data_plugins
    return render(request, "index.html", {"title": title, "plugini_ucitavanje": plagini_ucitavanje,
                                                  "plugini_vizualizacija": plagini_vizualizacija})


def odabir_plagina(request):

    if request.method == "GET":
        odabran_ucitavanje = request.GET['odabran_ucitavanje']
        odabran_vizualizacija = request.GET['odabran_vizualizacija']

        print("Za ucitavanje: " + odabran_ucitavanje)
        print("Za vizualizaciju: " + odabran_vizualizacija)

        if odabran_ucitavanje == "Odaberi" or odabran_vizualizacija == "Odaberi":
            print("Niste dobro odabrali plagine ili ih ni nema :(")
            return redirect('index')

        else:
            config = apps.get_app_config('core_django_app')
            config.chosen_load_plugin = config.load_data_plugins[odabran_ucitavanje]
            config.chosen_visualize_plugin = config.visualize_data_plugins[odabran_vizualizacija]
            return render(request, 'unos_parametara.html', {"title": "Unos parametara", "id": odabran_ucitavanje})


def pokretanje_plagina(request):

    putanja = request.GET["putanja"]
    print("Uneta putanja: " + putanja)
    if putanja is None or putanja == "":
        return redirect('index')

    #Initiating data loading
    plugin = apps.get_app_config('core_django_app').chosen_load_plugin
    plugin.load_data(putanja)

    config = apps.get_app_config('core_django_app')
    config.graph = plugin.graph

    #for v in plugin.graph.vertices():
     #   print(v)

    #TODO: OVDE POKRENUTI PLAGIN ZA VIZUALIZACIJU:
    if config.chosen_visualize_plugin.plugin_id() == "SimpleVisualization":
        return render(request, "visualization_proba.html", {"title": "Index",
                                                            "plagin": config.chosen_visualize_plugin,
                                                            "graf": config.graph})
    else:
        # TODO: ovde ce ici za Jelenin ComplexVisualisation
        return redirect('index')




# Ovo posle obrisati
# Dobar test korektne instalacije i ucitavanja plagina unutar CORE
def prikazi_plagine(request):
    config = apps.get_app_config('core_django_app')
    plagini_ucitavanje = config.load_data_plugins
    plagini_vizualizacija = config.visualize_data_plugins
    return render(request, "proba.html", {"title":"Index", "plugini_ucitavanje":plagini_ucitavanje,
                                          "plugini_vizualizacija": plagini_vizualizacija})



# # test SimpleVisualizaiton komponente sa Deezer podacima
# def simple_vis_proba(request):
#     config = apps.get_app_config('core_django_app')
#     plagin = config.visualize_data_plugins['SimpleVisualization']
#     graf = config.graph
#     return render(request, "visualization_proba.html", {"title": "Index", "plagin": plagin, "graf": graf})

