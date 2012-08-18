function channel_subscribe(channel) {
    pubnub = PUBNUB.init({
        publish_key: $("#pubnub").attr("pub-key"),
        subscribe_key: $("#pubnub").attr("sub-key"),
        ssl: false,
    });

    // LISTEN FOR MESSAGES
    pubnub.subscribe({
        channel    : channel,      // CONNECT TO THIS CHANNEL.
        restore    : false,              // STAY CONNECTED, EVEN WHEN BROWSER IS CLOSED
                                         // OR WHEN PAGE CHANGES.

        callback   : function(message) { // RECEIVED A MESSAGE.
            alert(message)
        },

        disconnect : function() {        // LOST CONNECTION.
            alert(
                "Connection Lost." +
                "Will auto-reconnect when Online."
            )
        },

        reconnect  : function() {        // CONNECTION RESTORED.
            alert("And we're Back!")
        },

        connect    : function() {        // CONNECTION ESTABLISHED.

            pubnub.publish({             // SEND A MESSAGE.
                channel : channel,
                message : "Hi from PubNub."
            })

        }
    })

}
