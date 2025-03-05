from flask import Flask, jsonify
from flask_smorest import Api
from marshmallow import ValidationError
from resources.song import blp as SongBlueprint

def create_app():
    app = Flask(__name__)

    app.config["API_TITLE"] = "Songs API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)
    api.register_blueprint(SongBlueprint)  # Neue Referenz zur Datei resources/song.py

    @app.errorhandler(ValidationError)
    def handle_marshmallow_error(error):
        return jsonify({"error": "Invalid data provided", "details": error.messages}), 400

    return app

if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0', port=8000)