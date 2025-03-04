from flask import Flask
from blueprints.endpoints import endpoints_blueprint  

app = Flask(__name__)

# Blueprint registrieren
app.register_blueprint(endpoints_blueprint)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)