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
//test
console.log(message);
            if (message.type == "student_connected") {
                console.log(message.name + " connected");
            } else {
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
