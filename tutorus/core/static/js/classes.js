function subscribeClassesChannel() {
    pubnub = getPubNubConn();
    pubnub.subscribe({
        channel: "classes",
        restore: false,

        callback: function(message) {
            // determine which type of message
            // and handle accordingly
            switch (message.type) {
            case "interest":
                setClassroomInterest(message);
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
        }
    });
}


function setClassroomInterest(message) {
    $("#interest-" + message.classroom).html(message.interest);
}
