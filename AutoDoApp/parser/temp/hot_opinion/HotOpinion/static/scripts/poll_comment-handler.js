function load_more_poll(){
    if(curr_page == total_page) return false;
    $.ajax({
        url: '/api/poll',
        data: {"page" : curr_page+1},
        success: handle_json_poll,
        error: function(error){
            console.log(error);
        },
        dataType: "json",
        contentType: "application/json; charset=utf-8"
    });
}

function handle_json_poll(json_data){
    curr_page += 1;
    var num_of_results = json_data.objects.length;
    for( var i = 0; i<num_of_results; i++){ // Poll level
        var poll_id = json_data.objects[i].poll_id;
        var title = json_data.objects[i].subject;
        var description = json_data.objects[i].question_statement;
        var div_item = make_poll_collapse(poll_id, title, description);
        make_poll_answers(poll_id, json_data.objects[i].questions, div_item);
        $("#accordion").append(div_item);
    }
}

function make_poll_collapse(poll_id, title, description){
    var heading_poll_id = "heading_poll" + poll_id;
    var collapse_poll_id = "collapse_poll" + poll_id;
    var sharp_collapse_poll_id = "#collapse_poll" + poll_id;
    var div_item = $("#collapse_top_div").clone();

    div_item.find(".panel-heading").attr("id", heading_poll_id);
    div_item.find("a.collapsed").attr("href", sharp_collapse_poll_id);
    div_item.find("a.collapsed").attr("aria-controls", collapse_poll_id);
    div_item.find("a.collapsed").text(title); // Poll Subject
    div_item.find(".panel-collapse").attr("id", collapse_poll_id);
    div_item.find(".panel-collapse").attr("aria-labelledby", heading_poll_id);
    div_item.find(".panel-body").text(description); // Poll Contents
    div_item.find("a.list-group-item").remove();

    return div_item;
}

function make_poll_answers(poll_id, answer_obj, div_item){
    var num_questions = answer_obj.length;
    for(var i=0; i<num_questions; i++){
        var answer_id = (i+1).toString();
        var li_str = "<a href=\"#\" class=\"list-group-item\" onclick=\"return vote_poll(" + poll_id +"," + answer_obj[i].id +")\">" + answer_id + ". " + answer_obj[i].answer_description+"</a>";
        div_item.find(".list-group").append(li_str);
    }
}
