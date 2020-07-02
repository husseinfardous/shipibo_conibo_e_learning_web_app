from flask import Flask
from flask import render_template, Response, request, jsonify, redirect, url_for, g

from flask_babel import Babel

from config import Config

from multilingual_bp import multilingual_bp

# set up flask app 
app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(multilingual_bp)

# set up babel
babel = Babel(app)
@babel.localeselector
def get_locale():
    if not g.get('lang_code', None):
        g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])
    return g.lang_code

@app.route("/", methods=["GET"])
def home():
    g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])
    return redirect(url_for('multilingual_bp.render_index_html'))

if __name__ == "__main__":
    app.run()
