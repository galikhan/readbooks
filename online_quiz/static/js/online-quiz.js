function getAnswer() 
{
    var answer = 0;
    var radio = $("input:radio[name='radio_values']:checked").val();
    if (radio != undefined) {
        answer = $("input:radio[name='radio_values']:checked").val();
    }
    else {
        return answer;
    }
    return answer;
}
function getAnswers(currentQuestionType)
{
    var array = Array();
//   var amountOfBlanks = $("#amount-of-blanks").val();
//   var amountOfMatchRows = $("#amount-of-match-rows").val();

    $("input:checkbox[name='checkbox_values']:checked").each(function(index){ 
        array[index] = $(this).val();
    });
    if( array.length == 0 ){ return array; }

    /*
    if( currentQuestionType == "single_answer" )
    {
        var radio = $("input:radio[name='radio_values']:checked").val();
        if( radio != undefined ){ array[0] = $("input:radio[name='radio_values']:checked").val(); }
        else{   return array;   } 
        
    } else if( currentQuestionType == "multiple_answer" ) {
        $("input:checkbox[name='checkbox_values']:checked").each(function(index){ 
            array[index] = $(this).val();
        });
        if( array.length == 0 ){ return array; }
        
    } else if( currentQuestionType == "true_false" ) {
    
        var radio = $("input:radio[name='radio_values']:checked").val();
        if( radio != undefined ){ array[0] = $("input:radio[name='radio_values']:checked").val(); }
        else{   return array;   } 
        
    } else if( currentQuestionType == "fill_in_blanks" ){
    
        for(var i = 0; i<amountOfBlanks; i++ ){
            array[i] = $("#fill_in_blanks_"+i).val();//         alert(array[i]);
        }
    } else if( currentQuestionType == "match_words" ){
        
        for(var i = 0; i<amountOfMatchRows; i++ ){
            array[i] = $("#match_words_"+i).val();//            alert(array[i]);
        }
    }*/
    return array;
}

//in usage
function enableButtonsAndPrintError() 
{
    $("#online-quiz-question-error-messages").html("<div style='padding:5px 0 5px 50px;border:1px solid red'>Select answer.</div>");
    $("#previous").removeAttr("disabled");
    $("#next").removeAttr("disabled");
    $("#skip").removeAttr("disabled");
}

//in usage
function disableAllButtons() 
{
    $("#next").attr("disabled", "disabled");
    $("#skip").attr("disabled", "disabled");
    $("#previous").attr("disabled", "disabled");
}
//in usage
function enableMathJax()
{
    var result = document.getElementById("online-quiz-question-area");
    MathJax.Hub.Queue(["Typeset", MathJax.Hub, result]);
}

function disableMe(id){
    $("#"+id).attr("disabled", "disabled");
}
function enableMe(id){
    $("#"+id).removeAttr("disabled");
}