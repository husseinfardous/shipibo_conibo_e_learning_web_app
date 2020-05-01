from flask import Flask
from flask import render_template, Response, request, jsonify, redirect, url_for
app = Flask(__name__)

# big data array :  all_entries
# array of dictionaries : target_entries
# single result dictionary: target_entry 

# dummy data
all_entries = [
            {'id':"0", 'spa_sentence':'hola me llamo janill y tengo veinte y dos anos y voy a la escuela de Columbia en la ciudad de nueva york', 'shi_sentence':'Hi My Name is Janill and I am twenty two years', 'alignment': {'nam':'llamo', 'jan':'janill', 'ill':'janill'},'shi_word_morphemes':'hi My Nam-e is Jan-ill and I am twen-ty two year-s old', 'shi_pos_tags': ['noun', 'subject', 'adverb', 'noun', 'verb']}, 
            {'id':"1", 'spa_sentence':'yo_1', 'shi_sentence':'I_1', 'shi_word_morphemes':'I-1', 'shi_pos_tags': ['noun', 'subject', 'adverb']}, 
            {'id':"2", 'spa_sentence':'yo_2', 'shi_sentence':'I_s', 'shi_word_morphemes':'I-2', 'shi_pos_tags': ['noun', 'subject', 'adverb']}, 
            {'id':"3", 'spa_sentence':'parafo_4', 'shi_sentence':'paragraph_4', 'shi_word_morphemes':'paragraph-4', 'shi_pos_tags': ['noun', 'subject', 'adverb']}, 
            {'id':"4", 'shi_sentence':'dummy', 'spa_sentence':'tonto', 'shi_word_morphemes':'dum-my', 'shi_pos_tags': ['noun', 'subject', 'adverb']},
            {'id':"5", 'spa_sentence':'hussein', 'shi_sentence':'hussein', 'shi_word_morphemes':'huss-e-in', 'shi_pos_tags': ['noun', 'subject', 'adverb']},
           ]

# data to keep 
language_setting = "ESPANOL"
target_entries = all_entries[0:3]


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

@app.route("/search", methods=['GET'])
def render_search_html():

    global target_entries 

    return render_template('aquinti_search.html', language_setting = language_setting, target_entries = target_entries)

# gets query from jquery and returns an array of sentences matching the query 
@app.route("/search_query_results", methods=['POST','GET'])
def search_query():

    global all_entries
    target_entries = []

    json_data = request.get_json()
    query = json_data['search_query']

    for shi_dict in all_entries:
        if query.lower() in shi_dict['shi_sentence'].lower():
            target_entries.append(shi_dict)

    return jsonify(target_entries = target_entries)

@app.route("/search/<id>", methods=['GET'])
def get_target_entry(id=id):

    global all_entries

    target_entry = all_entries[int(id)]

    return render_template('aquinti_result.html', language_setting = language_setting, target_entry = target_entry) 

if __name__ == '__main__':
    app.run()