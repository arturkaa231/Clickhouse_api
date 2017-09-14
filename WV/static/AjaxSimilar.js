

$('#post-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_post();
});




function create_post() {

    $.ajax({
        url : "/similarwords/", // the endpoint
        type : "POST", // http met
        data : {Data_id: $('#Data_id').val(), word: $('#word').val()}, // data sent with the post request

        // handle a successful response
        success : function(json) {
            $('#similarwords1').text(json.word1);
            $('#similarwords2').text(json.word2);
            $('#similarwords3').text(json.word3);
            $('#similarwords4').text(json.word4);
            $('#similarwords5').text(json.word5);
            $('#similarwords6').text(json.word6);
            $('#similarwords7').text(json.word7);// remove the value from the input
            console.log(json); // log the returned json to the console
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
