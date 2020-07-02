from flask import Blueprint, g, render_template, request, jsonify, current_app, abort
import json
from flask_babel import _, refresh


multilingual_bp = Blueprint('multilingual_bp', __name__, template_folder='templates', url_prefix='/<lang_code>')

app_data = None
with open("../data/app_corpus/data/app_data.json", "r") as app_data_file:
    app_data = json.load(app_data_file)


all_entries = [v for k, v in app_data.items()]

@multilingual_bp.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', g.lang_code)

@multilingual_bp.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.lang_code = values.pop('lang_code')

@multilingual_bp.before_request
def before_request():
    if g.lang_code not in current_app.config['LANGUAGES']:
        abort(404)

@multilingual_bp.route("/", methods=["GET"])
def render_index_html():
    return render_template("home.html")

@multilingual_bp.route("/about_team", methods=["GET"])
def render_about_team_html():
    return render_template("about_team.html")

@multilingual_bp.route("/search", methods=["GET", "POST"])
def render_search_html():

    global all_entries

    if request.method == "POST":

        
        target_entries = []
        json_data = request.get_json()
        query = json_data["search_query"]

        for shi_dict in all_entries:
            if query.lower() in shi_dict["shi_sentence"].lower():
                target_entries.append(shi_dict)

        return jsonify(target_entries=target_entries)
    
    else:

        target_entries = all_entries[0: 100]

        return render_template("aquinti_search.html", target_entries=target_entries)

@multilingual_bp.route("/result/<id>", methods=["GET"])
def get_target_entry(id):

    global all_entries

    target_entry = all_entries[int(id)]

    return render_template("aquinti_result.html", target_entry=target_entry)
