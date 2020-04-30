//used to change the language of the website 
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


$(document).ready(function(){

    // webpage language
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



});