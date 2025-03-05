from db import db

class SongModel(db.Model):  # Datenbank-Modell für SQL
    __tablename__ = "songs"  

    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(100), unique=True, nullable=False)  
    artist = db.Column(db.String(100), nullable=False)  
    genre = db.Column(db.String(100), nullable=False)  
    year = db.Column(db.Integer, nullable=False)  
    