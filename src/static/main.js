

$(document).ready(function(){

    // webpage language
    $('[lang="es"]').hide();

    $('#lang_link').click(function() {
        if ($('#lang_link').text() =='ESPAÑOL'){
            $('#lang_link').text('ENGLISH')
        }
        else{
            $('#lang_link').text('ESPAÑOL')
        }
        $('[lang="es"]').toggle();
        $('[lang="en"]').toggle();   
    });

});