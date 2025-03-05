from flask.views import MethodView
from flask_smorest import Blueprint, abort
from marshmallow import validate
import json
import os
from schemas import SongSchema

# Blueprint-Instanz erstellen
blp = Blueprint("songs", __name__, description="Operations on songs")

SONGS_FILE = 'songs.json'

######################################################################################
# Methoden zum Lesen/Schreiben 
def read_songs():
    """Read songs from JSON file, return an empty list if file does not exist."""
    if not os.path.exists(SONGS_FILE):
        return []  # Return empty list if file is missing
    with open(SONGS_FILE, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []  # Return empty list if JSON is invalid

def write_songs(songs):
    """Write songs to JSON file."""
    with open(SONGS_FILE, 'w') as file:
        json.dump(songs, file, indent=4)

######################################################################################
# API-Endpunkte
@blp.route('/songs')  # ❗ Richtig: "blp" statt "endpoints_blueprint"
class SongList(MethodView):
    """Manage the collection of songs"""

    @blp.response(200, SongSchema(many=True), description="Retrieve all songs")
    def get(self):
        """Fetch all songs from the database"""
        return read_songs()

    @blp.arguments(SongSchema)
    @blp.response(201, SongSchema, description="Add a new song")
    def post(self, new_song):
        """Add a new song to the collection (Title + Artist must be unique)"""
        songs = read_songs()
        if any(song['title'].lower() == new_song['title'].lower() and 
               song['artist'].lower() == new_song['artist'].lower() for song in songs):
            abort(400, message="A song with this title and artist already exists.")

        songs.append(new_song)
        write_songs(songs)
        return new_song

######################################################################################
#  Einzelne Songs abrufen, aktualisieren und löschen
@blp.route("/songs/<string:title>/<string:artist>")  # ❗ Richtig: "blp" statt "endpoints_blueprint"
class Song(MethodView):
    """Retrieve, update, or delete a song"""

    @blp.response(200, SongSchema, description="Retrieve a song by title & artist")
    def get(self, title, artist):
        """Retrieve a specific song based on title & artist"""
        song = next((song for song in read_songs() if song["title"].lower() == title.lower() 
                     and song["artist"].lower() == artist.lower()), None)
        if not song:
            abort(404, message="Song not found")
        return song

    @blp.arguments(SongSchema)
    @blp.response(200, SongSchema, description="Update a song (Title + Artist must remain unique)")
    def put(self, updated_data, title, artist):
        """Update a song while ensuring Title + Artist remain unique"""
        songs = read_songs()
        song_to_update = next((song for song in songs if song["title"].lower() == title.lower() 
                               and song["artist"].lower() == artist.lower()), None)

        if not song_to_update:
            abort(404, message="Song not found")

        # Check if new Title + Artist combination exists
        if "title" in updated_data or "artist" in updated_data:
            new_title = updated_data.get("title", song_to_update["title"]).lower()
            new_artist = updated_data.get("artist", song_to_update["artist"]).lower()

            if any(song["title"].lower() == new_title and 
                   song["artist"].lower() == new_artist for song in songs if song is not song_to_update):
                abort(400, message="A song with this title and artist already exists.")

        song_to_update.update(updated_data)
        write_songs(songs)
        return song_to_update

    @blp.response(200, description="Delete a song by title & artist")
    def delete(self, title, artist):
        """Delete a song from the collection"""
        songs = read_songs()
        new_songs = [song for song in songs if not (song["title"].lower() == title.lower() and 
                                                    song["artist"].lower() == artist.lower())]

        if len(new_songs) == len(songs):
            abort(404, message="Song not found")

        write_songs(new_songs)
        return {"message": "Deleted"}, 200