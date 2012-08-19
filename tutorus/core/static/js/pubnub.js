function getPubNubConn() {
    var pubnub = PUBNUB.init({
        publish_key: $("#pubnub").attr("pub-key"),
        subscribe_key: $("#pubnub").attr("sub-key"),
        ssl: false,
    });
    return pubnub;
}
