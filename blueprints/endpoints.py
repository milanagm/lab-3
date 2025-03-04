from flask import Blueprint, jsonify, request
import json

# Blueprint-Instanz erstellen
endpoints_blueprint = Blueprint('endpoints', __name__)

SONGS_FILE = 'songs.json'


#######################################################################################
# methoden
def read_songs():
    with open(SONGS_FILE, 'r') as file:
        return json.load(file)

def write_songs(songs):
    with open(SONGS_FILE, 'w') as file:
        json.dump(songs, file, indent=4)


#######################################################################################
# Endpoint: Alle Songs anzeigen
@endpoints_blueprint.route('/songs', methods=['GET'])
def view_songs():
    songs = read_songs()
    return jsonify(songs), 200

# Endpoint: Song hinzufügen
@endpoints_blueprint.route('/songs', methods=['POST'])
def add_song():
    new_song = request.get_json()
    songs = read_songs()
    for song in songs:
        if song['title'] == new_song['title'] and song['artist'] == new_song['artist']:
            return jsonify({'error': 'Song already exists'}), 400
    songs.append(new_song)
    write_songs(songs)
    return jsonify({'message': 'Song added successfully'}), 201

# Endpoint: Song ändern
@endpoints_blueprint.route('/songs/<string:title>/<string:artist>', methods=['PUT'])
def modify_song(title, artist):
    songs = read_songs()  
    updated_data = request.get_json()  

    for song in songs:
        if song['title'] == title and song['artist'] == artist:
            song.update(updated_data)
            write_songs(songs) 
            return jsonify({'message': 'Song updated successfully', 'song': song}), 200
    return jsonify({'error': 'Song not found'}), 404

# Endpoint: Song löschen
@endpoints_blueprint.route('/songs/<string:title>/<string:artist>', methods=['DELETE'])
def remove_song(title, artist):
    songs = read_songs()  

    updated_songs = [song for song in songs if not (song['title'] == title and song['artist'] == artist)]

    if len(updated_songs) == len(songs):
        return jsonify({'error': 'Song not found'}), 404

    write_songs(updated_songs)
    return jsonify({'message': 'Song removed successfully'}), 200