from flask import Flask
from flask_cors import CORS
from auth_routes import auth_blueprint
from movie_routes import movie_blueprint
from search_routes import search_blueprint

app = Flask(__name__)
# Enable cors for frontend app
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5501/", "https://www.google.ro"]}})

app.register_blueprint(auth_blueprint)
app.register_blueprint(movie_blueprint)
app.register_blueprint(search_blueprint)

# Only executed when calling the script directly
if __name__ == "__main__":
    app.run(debug=True)
