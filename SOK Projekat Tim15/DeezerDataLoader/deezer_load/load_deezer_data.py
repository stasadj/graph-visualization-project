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
    return path.replace("www", "api").replace("/us", "")


class LoadDeezerData(LoadDataService):
    """
    Class for extracting playlist data and stores it in a Graph
    """

    def __init__(self):
        super().__init__()
        self.graph = None
        self.artists = {}  # we keep artist ids here to prevent duplicates in case more songs are from the same artist

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
        self.graph = Graph(True)

        # Making initial request
        playlist = requests.get(path).json()
        #print(playlist)

        # Checking if playlist is private
        if "error" in playlist:
            print("private playlist!")
            return None

        playlist_attributes = {}
        playlist_attributes["title"] = playlist["title"]
        playlist_attributes["creator"] = playlist["creator"]["name"]
        playlist_attributes["duration"] = convert_seconds(playlist["duration"])
        playlist_attributes["picture"] = playlist["picture"]

        # Adding our root playlist vertex to graph
        playlist_vertex = self.graph.insert_vertex(playlist["type"], playlist_attributes, playlist["title"])

        # Now we iterate through the tracks of the playlist:
        for track in playlist["tracks"]["data"]:
            track_attributes = {}
            track_attributes["title"] = track["title_short"]
            track_attributes["duration"] = convert_seconds(track["duration"])
            track_attributes["album"] = track["album"]["title"]
            track_attributes["picture"] = track["album"]["cover"]

            # For each track we create a new vertex
            track_vertex = self.graph.insert_vertex(track["type"], track_attributes, track["title_short"])

            # Adding an edge between the playlist vertex and new track vertex
            self.graph.insert_edge(playlist_vertex, track_vertex)

            # Before creating new artist vertex, we check if such already exists
            if track["artist"]["id"] in self.artists.keys():
                #print(track_attributes)
                self.graph.insert_edge(track_vertex, self.artists[track["artist"]["id"]])
                continue

            # If the artist vertex doesnt already exist, we create a new one
            artist_attributes = {}
            artist_attributes["name"] = track["artist"]["name"]

            #TODO: Rethink getting the artist picture, as we have to send a new request for each track -> time consuming
            if playlist["nb_tracks"] <= 70:
                artistJson = requests.get(track["artist"]["link"].replace("www", "api")).json()
                artist_attributes["picture"] = artistJson["picture_medium"]

            # We add the artist vertex to graph and connect it to the track vertex
            artist_vertex = self.graph.insert_vertex(track["artist"]["type"], artist_attributes, track["artist"]["name"])
            self.graph.insert_edge(track_vertex, artist_vertex)

            # Now we save the artist vertex in case another track in the playlist has the same artist
            self.artists[track["artist"]["id"]] = artist_vertex

            print(artist_attributes)
            print(track_attributes)

        print("Number of vertices: " + str(self.graph.vertex_count()))
        for v in self.graph.vertices():
            print(v)
        for e in self.graph.edges():
            print(e)
        return self.graph





if __name__ == '__main__':
    some_playlist_path = "https://api.deezer.com/playlist/6033056424"
    some_playlist_path2 = "https://www.deezer.com/us/playlist/8433466142".replace("www", "api").replace("/us", "")

    deez = LoadDeezerData()
    #deez.load_data(some_playlist_path)
    #deez.load_data("https://www.deezer.com/us/playlist/8649081922")
