from flask import Flask
from flask import render_template, Response, request, jsonify, redirect, url_for
app = Flask(__name__)

language_setting = "ESPANOL"

@app.route("/", methods=['GET'])
def render_index_html():
    return render_template('home.html', language_setting = language_setting)

@app.route("/about_team", methods=['GET'])
def render_about_team_html():
    return render_template('about_team.html', language_setting = language_setting)

@app.route("/change_language", methods=['POST','GET'])
def change_language():

    global language_setting

    json_data = request.get_json()
    language_setting = json_data['new_language']

    return jsonify(language_setting=language_setting)

if __name__ == '__main__':
    app.run()