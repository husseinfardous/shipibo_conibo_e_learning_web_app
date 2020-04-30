from flask import Flask
from flask import render_template, Response, request, jsonify, redirect, url_for
app = Flask(__name__)

@app.route("/", methods=['POST','GET'])
def render_index_html():
    return render_template('home.html')

@app.route("/about_team", methods=['POST','GET'])
def render_about_team_html():
    return render_template('about_team.html')

if __name__ == '__main__':
    app.run()