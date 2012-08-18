function channel_subscribe(channel, username) {
    pubnub = PUBNUB.init({
        publish_key: $("#pubnub").attr("pub-key"),
        subscribe_key: $("#pubnub").attr("sub-key"),
        ssl: false,
    });

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
            case "new_question":
                addQuestion(message.question);
            default:
                console.log(message.type);
            }
        },

        disconnect: function() {
            $('#conn_status').html('<b>Closed</b>');
	    $('#conn_status').attr("class", "label label-warning")
        },

        reconnect: function() {
            $('#conn_status').html('<b>Connected</b>');
	    $('#conn_status').attr("class", "label label-success")
        },

        connect: function() {
            $('#conn_status').html('<b>Connected</b>');
	    $('#conn_status').attr("class", "label label-success")

            pubnub.publish({
                channel: channel,
                message: {"type": "student_connected", "name": username}
            })
        }
    });

    return pubnub;
}

function incrementStudentCount() {
    // get student count element
    // grab the value increment by 1
    // set value
}

function addQuestion(question) {
    // question added to asked list
    // if asked list greater then set #
    // remove older questions
}
