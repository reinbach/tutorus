$(function() {
    $("#new-questions").on("click", ".up_vote", function(event) {
        event.preventDefault();
        var question = $(this);
        $.ajax({
            type: "GET",
            url: $(this).attr("href"),
            success: function(data) {
                var d = $.parseJSON(data);
                $("#question-" + d.success).hide();
            },
            error: function(data, error) {
                alert(data);
                alert(error);
            }
        });
        return false;
    });
});

function subscribeClassRoomChannel(channel, username) {
    pubnub = getPubNubConn();
    pubnub.subscribe({
        channel: channel,
        restore: false,

        callback: function(message) {
            // determine which type of message
            // and handle accordingly
            switch (message.type) {
            case "student_connected":
                incrementStudentCount();
                console.log(message.name + " connected");
                break;
            case "new_question":
                addQuestion(message.question);
                break;
            default:
                console.log(message.type);
                break;
            }
        },
        disconnect: function() {
            $('#conn_status').html('<b>Closed</b>');
	    $('#conn_status').attr("class", "label label-warning");
        },

        reconnect: function() {
            $('#conn_status').html('<b>Connected</b>');
	    $('#conn_status').attr("class", "label label-success");
        },

        connect: function() {
            $('#conn_status').html('<b>Connected</b>');
	    $('#conn_status').attr("class", "label label-success");
            pubnub.publish({
                channel: channel,
                message: {"type": "student_connected", "name": username}
            });
        }
    });
}

function incrementStudentCount() {
    // get student count element
    // grab the value increment by 1
    // set value
}

function addQuestion(question) {
    // question added to asked list
    q = "<li id='question-" + question.pk + "'> \
      <h4> \
        <a href='" + question.up_vote_url + "' class='up_vote'> \
          <span class='label label-success'><i class='icon-arrow-up'></i></span> \
        </a> \
        " + question.subject + " \
      </h4> \
      <blockquote> \
        <p>" + question.content + "</p> \
        <small> " + question.student  + "</small> \
      </blockquote> \
    </li>";
    $("#new-questions").prepend(q);
    // if asked list greater then set #
    // remove older questions
    if ($("#new-questions li").length > parseInt($("#max_new_question_count").text())) {
        $("#new-questions li:last").remove();
    }
}
