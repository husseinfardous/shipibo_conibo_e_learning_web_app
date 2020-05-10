import json

from flask import Flask
from flask import render_template, Response, request, jsonify, redirect, url_for

app = Flask(__name__)

app_data = None

with open("../data/app_corpus/data/app_data.json", "r") as app_data_file:
    app_data = json.load(app_data_file)

language_setting = "ESPANOL"

all_entries = [v for k, v in app_data.items()]

@app.route("/", methods=["GET"])
def render_index_html():
    return render_template("home.html", language_setting=language_setting)

@app.route("/about_team", methods=["GET"])
def render_about_team_html():
    return render_template("about_team.html", language_setting=language_setting)

@app.route("/change_language", methods=["POST","GET"])
def change_language():

    global language_setting

    json_data = request.get_json()
    language_setting = json_data["new_language"]

    return jsonify(language_setting=language_setting)

@app.route("/search", methods=["GET", "POST"])
def render_search_html():

    global all_entries

    if request.method == 'POST':
        
        target_entries = []
        json_data = request.get_json()
        query = json_data["search_query"]

        for shi_dict in all_entries:
            if query.lower() in shi_dict["shi_sentence"].lower():
                target_entries.append(shi_dict)

        return jsonify(target_entries=target_entries)
    else:

        target_entries = all_entries[0: 100]

        return render_template("aquinti_search.html", language_setting=language_setting, target_entries=target_entries)

@app.route("/result/<id>", methods=["GET"])
def get_target_entry(id):

    global all_entries

    target_entry = all_entries[int(id)]

    return render_template("aquinti_result.html", language_setting=language_setting, target_entry=target_entry)

if __name__ == "__main__":
    app.run()