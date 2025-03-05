from marshmallow import Schema, fields, validate

# Vordefinierte Genres für die Validierung
GENRE_CHOICES = ["Pop", "Rock", "Jazz", "Hip-Hop", "Classical", "Electronic", "Country", "Blues", "Folk", "Reggae"]

# Marshmallow Schema mit Validierung
class SongSchema(Schema):
    title = fields.String(required=True, metadata={"description": "The title of the song"})
    artist = fields.String(required=True, metadata={"description": "The name of the artist"})
    genre = fields.String(required=True, validate=validate.OneOf(GENRE_CHOICES),
                          metadata={"description": "Genre of the song (must be one of the predefined genres)"})
    year = fields.Integer(required=True, validate=validate.Range(min=1900, max=2025),
                          metadata={"description": "The release year of the song (1900-2025)"})