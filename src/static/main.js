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
        url: "change_language",
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

    shipibo_query = search_query

    new_data = {'search_query': shipibo_query}

    $.ajax({
        type: "POST",
        url: "search_query_results",
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
        url: '/search/' + entry_id,
        success: function(result) {
            window.location.href =  '/search/' + entry_id
        }
    });
}

/************************************** Result Webpage ****************************************/
function populate_shi_sentence(shi_sentence, named_entity_dict, syllables_dict){
    console.log(named_entity_dict)
    sentence = shi_sentence.charAt(0).toUpperCase() + shi_sentence.substr(1).toLowerCase()
    word_array = sentence.split(" ")
    $.each(word_array, function(index, word){
        var span_word = $("<span class='original-shi-word'>"+ word +"</span>")
        $(span_word).click(function(){
            var lowercased_word = word.toLowerCase().replace(/[.,\/#?!$%\^&\*;:{}=\-_`~()]/g,"")
            $(".chosen-word").html(lowercased_word)
            $(".named-entity").html(named_entity_dict[lowercased_word])
            $(".syllable-breakdown").html(syllables_dict[lowercased_word])

        });
        $(".original-shi-sentence").append(span_word)
    })
}



/*
function populate_word_pos_tag(morphemes, tags){
    var morphemes_array = morphemes.split(" ")
    var count = 0 

    $.each(morphemes_array, function(index, word){
        if (count < tags.length && word != '.' && word != '!' && word != '?' && word != ',' && word != ';'){
            var shipibo_word = $("<div class='shipibo-word'> " + word  + "</div>")
            var pos_tag = $("<div class='shipibo-word'> " + tags[count]  + "</div>")
            count = count + 1
        }
        else{
            var shipibo_word = $("<div class='shipibo-word'> " + word  + "</div>")
            var pos_tag = $("<div class='pos-tag'>"+ "-" + "</div>")
        }

        var word_pos_tag = shipibo_word.append(pos_tag)
        var div = $("<div class='word-container'> </div>").append(word_pos_tag)

        $(".shipibo-conibo-segmented-sentence").append(div)
         
    })
   

}
*/

function populate_word_pos_tag(morphemes, tags, alignment_dict, spa_sent){
    var morphemes_array = morphemes.split(" ")
    var count = 0 

    var spanish_word_values = []
    var spanish_colors={}
    var color_classes = ["background-pink","background-blue", "background-orange", "background-purple", "background-green", "background-grey","background-red", "background-bright-green", "background-bright-purple", "background-bright-orange","background-bright-yellow",  "background-yellow"]

    for (key in alignment_dict){
        if (!(key in spanish_word_values)){
            spanish_word_values.push(alignment_dict[key])
        }
    }

    $.each(spanish_word_values, function(index, word){
        spanish_colors[word.toLowerCase()] = color_classes[index]
    })

    var spa_sent_words = spa_sent.split(" ")

    $.each(spa_sent_words, function(index, word){
        if (word.toLowerCase().replace(/[.,\/#?!$%\^&\*;:{}=\-_`~()]/g,"") in spanish_colors){
            var color = spanish_colors[word.toLowerCase().replace(/[.,\/#?!$%\^&\*;:{}=\-_`~()]/g,"")]
            var div = $("<div class=' spanish-word "+ color + "'> " + word +" </div>")
            $(".spanish-segmented-sentence").append(div)
        }
        else{
            var div = $("<div class='spanish-word '> " + word +" </div>")
            $(".spanish-segmented-sentence").append(div)
        }
    })


    
    $.each(morphemes_array, function(index, word){
        var colored_word = ""

        var morphemes = word.split("-")
        $.each(morphemes, function(index, m){
            var morpheme_color_class = ''
            var original_m = m 
            var m = m.toLowerCase()
            if ( m in alignment_dict){
                spa_word = alignment_dict[m]
                morpheme_color_class = spanish_colors[spa_word]

                if (index != 0){
                    colored_word = colored_word + "-" + '<span class=' + morpheme_color_class +'>' + original_m + '</span>'
                }
                else{
                    colored_word = colored_word + " " + '<span class=' + morpheme_color_class +'>' + original_m + '</span>'
                }
            }
            else{
                if (index != 0){
                    colored_word = colored_word + "-" + m
                }
                else{
                    colored_word = colored_word + " " + m
                }
       
            }
        })
        

        if (count < tags.length && word != '.' && word != '!' && word != ',' && word != ';'){
            var shipibo_word = $("<div class='shipibo-word'> " + colored_word  + "</div>")
            var pos_tag = $("<div class='pos-tag'> " + tags[count]  + "</div>")
            count = count + 1
            colored_word = ""
        }
        else{
            var shipibo_word = $("<div class='shipibo-word'> " + word  + "</div>")
            var pos_tag = $("<div class='pos-tag'>"+ "-" + "</div>")
        }

        var word_pos_tag = shipibo_word.append(pos_tag)
        var div = $("<div class='word-container'> </div>").append(word_pos_tag)

        $(".shipibo-conibo-segmented-sentence").append(div)
         
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

    if(window.location.pathname.search(/search/) > -1 ){
        populate_shi_sentence(target_entry['shi_sentence'], target_entry['shi_named_entities'], target_entry['shi_word_syllables'])
        populate_word_pos_tag(target_entry['shi_word_morphemes'], target_entry['shi_pos_tags'], target_entry['alignment'],target_entry['spa_sentence'] )

    }

});