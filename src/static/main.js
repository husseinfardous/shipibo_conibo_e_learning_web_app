/************************************** All Webpages ****************************************/

//manages language of the website 
function change_language(lang_set){

    var new_language = ''
    if (lang_set === 'ESPANOL'){
        new_language = 'ENGLISH'
    }
    else{
        new_language = 'ESPANOL'
    }

    new_data = {'new_language': new_language}

    $.ajax({
        type: "POST",
        url: "/change_language",
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(new_data),
        success: function(result){
            language_setting = result['language_setting']
            if (language_setting ==='ESPANOL'){
                $('#lang_link').text('ENGLISH')
            }
            else{
                $('#lang_link').text('ESPAÑOL')
            }
        },
    });
}

/************************************** Search Webpage ****************************************/

// displays shipibo sentences on the search page 
function display_shi_sentences(shi_entries, search_query){

    $('#search-results').empty();
    $('#entries-num').empty();
    $('#query').empty();

    $('.entries-num').html(shi_entries.length)
    $('.query').html( ' " ' + search_query + ' " ')


    span_beg = "<span class='bold-text'>"
    span_end = "</span>" 

    $.each(shi_entries, function(index, shi_dictionary){
        
        shi_sentence = shi_dictionary['shi_sentence']

        if (search_query != ""){
            position = 0 
            $.each(shi_sentence.match(new RegExp(search_query, 'gi')), function(i,word){
                position = shi_sentence.indexOf(word, position)
                shi_sentence = shi_sentence.substring(0, position) +  span_beg + word + span_end + shi_sentence.substring(position + word.length, shi_sentence.length)
                position = position + span_beg.length + span_end.length
            });
        }

        shi_sentence_div = $("<div class='shi-sentence'> " + shi_sentence  + "</div>")

        $(shi_sentence_div).hover(function(){
            $(this).addClass("sentence-hover")
            }, function(){
            $(this).removeClass("sentence-hover")
          });
        $(shi_sentence_div).click(function(){
            get_target_entry(shi_entries[index]['id'])
        });
        $('#search-results').append(shi_sentence_div)
    })
}

// sends a query to flask in order to get an array of shipibo sentences
function retrieve_shipibo_sentences(search_query){

    var shipibo_query = search_query

    var new_data = {'search_query': shipibo_query}

    $.ajax({
        type: "POST",
        url: "search",
        dataType : "json",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(new_data),
        success: function(result){
            target_entries = result['target_entries']
            display_shi_sentences(target_entries, shipibo_query)

        },
    });
}

function get_target_entry(entry_id){
    $.ajax({
        url: '/result/' + entry_id,
        success: function(result) {
            window.location.href =  '/result/' + entry_id
        }
    });
}

/************************************** Result Webpage ****************************************/
var eng_span_pos_tags = {'ADJ':'adjetivo', 'ADV':'adverbio', 'CONJ':'conjución', "DET":"determinante", "INTJ":"interjección", "NOUN":"nombre", "PROPN":"nombre propio", "NUM":"numeral","onm":"ONOMATOPEYA","INTW":"palabra interrogativa", "ADP":"postposición", "PRON":"pronombre", "PUNCT":"punctuación","SYM":"símbolo", "VERB":"verbo","AUX":"verbo auxiliar", "desconocido":"desconocido"}
var color_class_list = ["background-purple", "background-cyan", "background-light-orange", "background-red", "background-yellow", "background-green", "background-pink", "background-blue", "background-blue-green","background-grey", "background-sand", "background-earth-green"]
var punctuations = [".", ",", ":", "!", "?", "¿", "¡"]

function display_chosen_shi_sentence(chosen_shi_sentence){
    $(".original-shi-sentence").append(chosen_shi_sentence)
}

// creates a dictionary that assigns each spanish word a color class
function map_spa_word_to_color(alignment_dictionary){

    var spanish_word_color_class = {} 
    var count = 0 
    for (k in alignment_dictionary){
        spanish_word_color_class[k] = color_class_list[count]
        count = count + 1 
    }

    return spanish_word_color_class
}

// creates a dictionary that maps each shi morpheme index to its span word alignment
function map_shi_morph_index_to_color(alignment_dictionary, spa_word_color){
 
    shi_morph_index_spa_dict = {}
    $.each(alignment_dictionary, function(key, value){
        for (i in value){
            shi_morph_index_spa_dict[value[i]] = spa_word_color[key] 
        }
    })

    return shi_morph_index_spa_dict
}

// displays spanish words and pos tags with respective colors
function  display_spanish_alignment_sentence(word_to_color, spa_tok_sentence, spa_pos_tag_arr){

    var spa_tok_array = spa_tok_sentence.split(" ")
 
    var capitalized = false
    $.each(spa_tok_array, function(i, value){
        
        // color class for spa word 
        var color = ""
        if (value in word_to_color){
            color = word_to_color[value]
        }

        // spanish pos tag of the word 
        var spanish_pos_tag = ""
        if ( spa_pos_tag_arr[i] in eng_span_pos_tags){
            spanish_pos_tag = eng_span_pos_tags[spa_pos_tag_arr[i]]
        }
        else{
            spanish_pos_tag = spa_pos_tag_arr[i]
        }

        var div_string = ""
        // if the token is a punctation
        if (value in  punctuations){
            div_string = "<div class='punct " + color + "'>" + value + "</div>"
        }
        else{ //if token is a spanish word 
            if (capitalized === false){
                div_string = "<div class='word " + color + "'>" + value.substr(0,1).toUpperCase() + value.substr(1) + "</div>"
                capitalized = true
            }
            else{
                div_string = "<div class='word " + color + "'>" + value + "</div>"
            }
        }
        
        var empty_div = $("<span class='word-container'></span>")
        var spa_word = $(div_string)
        var pos_tag_div_en = $("<div class='pos-tag'>" + spa_pos_tag_arr[i] + "</div>")
        var pos_tag_div_spa = $("<div class='pos-tag'>" + spanish_pos_tag + "</div>")

        empty_div.append(spa_word)
        empty_div.append(pos_tag_div_en)
        empty_div.append(pos_tag_div_spa)

        $(".spanish-segmented-sentence").append(empty_div)

    })
}

function display_shipibo_alignment_sentence(morph_index_to_color, shi_tok_sentence, shi_word_morphemes, shi_pos_tag_arr, grp_indices, shi_named_entities, shi_word_syllables){
    console.log(grp_indices)
    console.log(morph_index_to_color)
    var shi_tok_morph_array = shi_word_morphemes.split(" ")
    var tok_sentence = shi_tok_sentence.split(" ")

    var capitalized = false
    $.each(grp_indices, function(index, array_of_indices){

        var color = ""
        var div_string = ""
        var word_string = ""

        $.each(array_of_indices, function(i, value){
            
            
            // color class for morpheme
            color = ""
            if (value in morph_index_to_color){
                color = morph_index_to_color[value]
            }
            
            console.log(color + " " + i + " " + value )

            // if the token is a punctation
            if ( shi_tok_morph_array[value] in  punctuations){
                div_string = "<span class=' " + color + "'>" + shi_tok_morph_array[value] + "</span>"
            }
            else{ //if token is a shi word 
                if (capitalized === false){
                    div_string = "<span class=' " + color + "'>" + shi_tok_morph_array[value].substr(0,1).toUpperCase() + shi_tok_morph_array[value].substr(1) + "</span>"
                    capitalized = true
                }
                else{
                    div_string = "<span class=' " + color + "'>" + shi_tok_morph_array[value] + "</span>"
                }
            }

            if (array_of_indices.length != 1 && i < array_of_indices.length-1){
                div_string = div_string + " - "  
            }

            word_string = word_string + div_string
        
        })

        // spanish pos tag of the word 
        var spanish_pos_tag = ""
        if ( shi_pos_tag_arr[index] in eng_span_pos_tags){
            spanish_pos_tag = eng_span_pos_tags[shi_pos_tag_arr[index]]
        }
        else{
            spanish_pos_tag = shi_pos_tag_arr[index]
        }

        //append elements to html element on page
        var empty_div = $("<span class='word-container'></span>")
        var shi_word = $("<span class='word' >" + word_string + "</span>")

        $(shi_word).click(function(){
            $(".named-entity").html(shi_named_entities[tok_sentence[index]])
            $(".syllable-breakdown").html(shi_word_syllables[tok_sentence[index]])
        });

        $(shi_word).hover(function(){
            $(this).addClass("word-hover")
            }, function(){
            $(this).removeClass("word-hover")
          });

        var pos_tag_div_en = $("<div class='pos-tag'>" + shi_pos_tag_arr[index] + "</div>")
        var pos_tag_div_spa = $("<div class='pos-tag'>" + spanish_pos_tag + "</div>")

        empty_div.append(shi_word)
        empty_div.append(pos_tag_div_en)
        empty_div.append(pos_tag_div_spa)

        $(".shi-segmented-sentence").append(empty_div)

    })
}





$(document).ready(function(){

    /************************************** all pages ****************************************/
    // language setting (applicable for every page)
    if (language_setting === "ESPANOL"){
        $('[lang="en"]').hide();
        $('#lang_link').text('ENGLISH');
    }
    else{
        $('[lang="es"]').hide();
        $('#lang_link').text('ESPAÑOL'); 
    }

    $('#lang_link').click(function(){
        change_language(language_setting);
        $('[lang="es"]').toggle();
        $('[lang="en"]').toggle(); 
    });

    /************************************** Search Page ****************************************/

    if(window.location.pathname == '/search'){

        // displays initial 10 sentences on the interface
        display_shi_sentences(target_entries, "")

        // displays shipibo sentences on the interface after the user inputs a query 
        $('#submit-button-en').click(function(event){
            var shipibo_query = $("#shipibo-input-en").val();

            if (shipibo_query != ""){
                $("#shipibo-input-en").val('')
                retrieve_shipibo_sentences(shipibo_query)
            }
            else{
                $("#shipibo-input-es").focus()
            }
        }); 

        $('#submit-button-es').click(function(event){
            var shipibo_query = $("#shipibo-input-es").val();
            if (shipibo_query != ""){
                $("#shipibo-input-es").val('')
                retrieve_shipibo_sentences(shipibo_query)
            }
            else{
                $("#shipibo-input-es").focus()
            }
        }); 

    }

    if(window.location.pathname.search(/result/) > -1 ){

        var spa_word_to_color = map_spa_word_to_color(target_entry['alignment'])
        var shi_index_to_color = map_shi_morph_index_to_color(target_entry['alignment'], spa_word_to_color )

        display_chosen_shi_sentence(target_entry['shi_sentence'])
        display_spanish_alignment_sentence(spa_word_to_color, target_entry['spa_tok_sentence'], target_entry['spa_pos_tags'])
        display_shipibo_alignment_sentence(shi_index_to_color, target_entry['shi_tok_sentence'], target_entry['shi_word_morphemes'], target_entry['shi_pos_tags'], target_entry['shi_morph_grps_indices'], target_entry['shi_named_entities'], target_entry['shi_word_syllables'])
    }

});