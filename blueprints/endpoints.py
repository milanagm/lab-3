from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import Schema, fields
import json

# Blueprint-Instanz erstellen
endpoints_blueprint = Blueprint("songs", __name__, description="Operations on songs")

SONGS_FILE = 'songs.json'


######################################################################################
# methoden
def read_songs():
    with open(SONGS_FILE, 'r') as file:
        return json.load(file)

def write_songs(songs):
    with open(SONGS_FILE, 'w') as file:
        json.dump(songs, file, indent=4)


#######################################################################################
# schema zum abgleichen
class SongSchema(Schema):
    title = fields.String(required=True)
    artist = fields.String(required=True)
    genre = fields.String(required=True)
    year = fields.String(required=True)

#######################################################################################

# Endpoint: Alle Songs anzeigen und adden
@endpoints_blueprint.route('/songs')
class SongList(MethodView):
    @endpoints_blueprint.response(200, SongSchema(many=True))
    def get(self):
        return read_songs()

    @endpoints_blueprint.arguments(SongSchema)
    @endpoints_blueprint.response(201, SongSchema)
    def post(self, new_song):

        """ Neuen Song adden (Unique pro artist)"""

        songs = read_songs()
        if any(song['title'].lower() == new_song['title'].lower() and song['artist'].lower() == new_song['artist'].lower() for song in songs):
            abort(400, message= "A song with this title already exists for this artist." )
        songs.append(new_song)
        write_songs(songs)
        return new_song
    

# Einzelne Songs abrufen, aktualisieren und löschen
@endpoints_blueprint.route("/songs/<string:title>/<string:artist>")
class Song(MethodView):
    @endpoints_blueprint.response(200, SongSchema)
    def get(self, title, artist):
        """Song per Titel & Artist abrufen"""
        song = next((song for song in read_songs() if song["title"].lower() == title.lower() and song["artist"].lower() == artist.lower()), None)
        if not song:
            abort(404, message="Song not found")
        return song

    @endpoints_blueprint.arguments(SongSchema)
    @endpoints_blueprint.response(200, SongSchema)
    def put(self, updated_data, title, artist):
        """Song aktualisieren (Unique pro Artist)"""
        songs = read_songs()
        song_to_update = next((song for song in songs if song["title"].lower() == title.lower() and song["artist"].lower() == artist.lower()), None)

        if not song_to_update:
            abort(404, message="Song not found")

        # Check for title uniqueness if the title is being updated
        if "title" in updated_data:
            if any(song["title"].lower() == updated_data["title"].lower() and song["artist"].lower() == artist.lower() for song in songs if song is not song_to_update):
                abort(400, message="A song with this title already exists for this artist.")

        song_to_update.update(updated_data)
        write_songs(songs)
        return song_to_update

    def delete(self, title, artist):
        """Song löschen"""
        songs = read_songs()
        new_songs = [song for song in songs if not (song["title"].lower() == title.lower() and song["artist"].lower() == artist.lower())]

        if len(new_songs) == len(songs):
            abort(404, message="Song not found")

        write_songs(new_songs)
        return {"message": "Deleted"}, 200