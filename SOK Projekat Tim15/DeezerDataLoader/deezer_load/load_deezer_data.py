from core_django_app.models import Graph
from core_django_app.services.services import LoadDataService

import datetime
import requests


def convert_seconds(seconds):
    """
    Function which converts seconds to HH:mm:ss string format
    :param seconds: seconds to be converted
    :return: correct format string
    """
    conversion = datetime.timedelta(seconds=seconds)
    return str(conversion)


def fix_path(path):
    """
    Method which corrects deezer domain paths for the API
    :param path: input path
    :return: fixed path
    """
    return path.replace("www", "api").replace("/us", "").replace("/en", "")


class LoadDeezerData(LoadDataService):
    """
    Class for extracting playlist data and stores it in a Graph
    """

    def __init__(self):
        super().__init__()
        self._graph = None
        self._artists = {}  # we keep artist ids here to prevent duplicates in case more songs are from the same artist

    def name(self):
        return 'LoadDeezerData'

    def plugin_id(self):
        return 'DeezerDataLoader'

    def load_data(self, path) -> Graph:

        """
        Method for Deezer data extraction and Graph class object creation
        :param path: a Deezer playlist path
        :return: Graph object
        """
        path = fix_path(path)
        self._graph = Graph(True)
        self._artists = {}

        # Making initial request
        playlist = requests.get(path).json()

        # Checking if playlist is private
        if "error" in playlist:
            return None

        playlist_attributes = {}
        playlist_attributes["title"] = playlist["title"]
        playlist_attributes["description"] = playlist["description"]
        playlist_attributes["creator"] = playlist["creator"]["name"]
        playlist_attributes["duration"] = convert_seconds(playlist["duration"])
        playlist_attributes["nb_tracks"] = playlist["nb_tracks"]

        # Adding our root playlist vertex to graph
        playlist_vertex = self._graph.insert_vertex(playlist["type"], playlist_attributes, playlist["title"])

        # Now we iterate through the tracks of the playlist:
        for track in playlist["tracks"]["data"]:
            track_attributes = {}
            track_attributes["title"] = track["title_short"]
            track_attributes["duration"] = convert_seconds(track["duration"])
            track_attributes["album"] = track["album"]["title"]
            track_attributes["rank"] = track["rank"]

            # For each track we create a new vertex
            track_vertex = self._graph.insert_vertex(track["type"], track_attributes, track["title_short"])

            # Adding an edge between the playlist vertex and new track vertex
            self._graph.insert_edge(playlist_vertex, track_vertex)

            # Before creating new artist vertex, we check if such already exists
            if track["artist"]["id"] in self._artists.keys():
                self._graph.insert_edge(track_vertex, self._artists[track["artist"]["id"]])
                continue

            # If the artist vertex doesnt already exist, we create a new one
            artist_attributes = {}
            artist_attributes["name"] = track["artist"]["name"]


            # We add the artist vertex to graph and connect it to the track vertex
            artist_vertex = self._graph.insert_vertex(track["artist"]["type"], artist_attributes, track["artist"]["name"])
            self._graph.insert_edge(track_vertex, artist_vertex)

            # Now we save the artist vertex in case another track in the playlist has the same artist
            self._artists[track["artist"]["id"]] = artist_vertex

        return self._graph

