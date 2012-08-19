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
                console.log(data);
                console.log(error);
            }
        });
        return false;
    });

    $("#top-questions").on("submit", "form", function(event) {
        event.preventDefault();
        var answer = $(this);
        $.ajax({
            type: "POST",
            url: answer.attr("action"),
            data: answer.serializeArray(),
            success: function(data) {
                answer.hide();
            },
            error: function(data, error) {
                console.log(data);
                console.log(error);
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
                break;
            case "new_question":
                addQuestion(message.question);
                break;
            case "top_question":
                setTopQuestions(message.questions);
                break;
            case "answer_question":
                answerQuestion(message.question);
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
    var count = parseInt($("#student_count").text());
    count += 1;
    $("#student_count").text(count);
}

function createQuestion(question) {
    q = "<li id='question-" + question.pk + "'> \
      <h4>";

    if (question.up_vote_url) {
        q += "<a href='" + question.up_vote_url + "' class='up_vote'> \
          <span class='label label-success'><i class='icon-arrow-up'></i></span> \
          </a>";
    }

    if (question.vote_count) {
        q += "<span class='label label-success'>" + question.vote_count + "</span>";
    }

    q += " " + question.subject + " \
      </h4> \
      <blockquote> \
        <p>" + question.content + "</p> \
        <small> " + question.student  + "</small> \
      </blockquote>";

    if (question.answer) {
        q += "<blockquote> \
        <p>" + question.answer + "</p> \
        <small> Tutor</small> \
      </blockquote>";
    }

    q += "</li>";
    return q;
}
function addQuestion(question) {
    // question added to asked list
    q = createQuestion(question);
    $("#new-questions").prepend(q);
    // if asked list greater then set #
    // remove older questions
    if ($("#new-questions li").length > parseInt($("#max_new_question_count").text())) {
        $("#new-questions li:last").remove();
    }
}

function setTopQuestions(questions) {
    // for now to reload the top questions
    var top_question = $("#top-questions");
    top_question.find("li").remove();
    for (i = 0; i <= questions.length; i++) {
        q = createQuestion(questions[i]);
        top_question.append(q);
    }
}

function answerQuestion(question) {
    q = createQuestion(question);
    $("#answer-questions").append(q);
}
