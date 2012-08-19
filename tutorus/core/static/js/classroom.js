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

    $("#scratchpad_form").on("submit", function(event) {
        event.preventDefault();
        var scratchpad = $(this);
        $.ajax({
            type: "POST",
            url: scratchpad.attr("action"),
            data: scratchpad.serializeArray(),
            success: function(data) {
                console.log(data);
            },
            error: function(data, error) {
                console.log(data);
                console.log(error);
            }
        });
        return false;
    });

    $(".steps").on("click", "li", function() {
        var step_url = $(this).attr("step_url");
        publishNextStep(step_url);
    });

    $('.btnNext').on('click', function(event) {
        event.preventDefault();
        nextTab();
    });

    $('.btnPrev').on('click', function() {
        event.preventDefault();
        prevTab();
    });

    $('a[data-toggle="tab"]').on('shown', function (e) {
        isLastTab();
        isFirstTab();
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
                break;
            case "scratchpad":
                setScratchpad(message);
                break;
            case "step":
                if (message.data == "next") {
                    nextTab();
                } else {
                    prevTab();
                }
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
        q += "<h5>Answer</h5> \
        <blockquote> \
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
    for (i = 0; i < questions.length; i++) {
        q = createQuestion(questions[i]);
        top_question.append(q);
    }
}

function answerQuestion(question) {
    q = createQuestion(question);
    $("#answered-questions").append(q);
    // remove question from top questions
    $("#top-question-" + question.pk).hide();
}

function setScratchpad(message) {
    $("#scratchpad_form textarea").html(message.data);
}

function publishNextStep(url) {
    $.ajax({
        type: "GET",
        url: url,
    });
}

function nextTab() {
    var e = $('#steps li.active').next().find('a[data-toggle="tab"]');
    if (e.length > 0) {
        e.click();
    }
    publishNextStep(e.attr("href"));
    isLastTab();
}

function prevTab(elem) {
    var e = $('#steps li.active').prev().find('a[data-toggle="tab"]');
    if(e.length > 0) e.click();
    publishNextStep(e.attr("href"));
    isFirstTab();
}

function isLastTab() {
    var e = $('#steps li:last').hasClass('active');

    if( e ){
        $('.btnNext').hide();
    }else{
        $('.btnNext').show();
    }
    return e;
}

function isFirstTab() {
    var e = $('#steps li:first').hasClass('active');
    if( e ){
        $('.btnPrev').hide();
    }else{
        $('.btnPrev').show();
    }
    return e;
}
