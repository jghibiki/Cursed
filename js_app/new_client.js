
var client = {
    _: {
        id: Math.random().toString(36).substring(7),
        subs: {},
        ack: {},
        ack_once: {},
        once: {},
        init_hooks: [],
        username: "jghibiki",
        password: "1111",
        debug: false 
    },
    init: function(){
        client.ws = new WebSocket("ws://localhost:9000")
        client.ws.onopen = function(event){
            client.send({"type": "ping"});
            client.send({"type": "register"});

            client.send({
                "type": "command",
                "key": "register.user",
                "details": {
                    "username": client._.username,
                    "current_map": null
                }
            });

            for(var callback of client._.init_hooks){
                callback();
            }
        };
        client.ws.onmessage = function(event){
            var data = JSON.parse(event.data);
            if(client._.debug){
                console.log(event.data);
            }

            if(data.type == "pong"){ //handle ping pong
                console.log("pong");
            }
            else if(data.type == "broadcast"){
                if(client._.subs.hasOwnProperty(data.key)){
                    for(var sub of client._.subs[data.key]){ //handle global broadcast
                        sub(data);
                    }
                }
                if(client._.once.hasOwnProperty(data.key)){
                    for(var sub of client._.once[data.key]){
                        sub(data);
                    }
                    client._.once[data.key] = [];
                }
            }
            else if(data.type == "broadcast_target"  // handle targeted broadcast
                && data.targets.indexOf(client._.id) > -1){
                if(client._.subs.hasOwnProperty(data.key)){
                    for(var sub of client._.subs[data.key]){
                        sub(data);
                    }
                }
                if(client._.once.hasOwnProperty(data.key)){
                    for(var sub of client._.once[data.key]){
                        sub(data);
                    }
                    client._.once[data.key] = [];
                }
            }
            else if(data.type == "acknowledge"){
                if(client._.debug){
                    console.log("Server acknowledged request for: " + data.key);
                }
                if(client._.ack.hasOwnProperty(data.key)){
                    for(var sub of client._.ack[data.key]){
                        sub(data);
                    }
                }
            }
            else if(data.type == "error"){
                console.log(data)
            }
        }
    },
    subscribe: function(key, callback){
        if(!client._.subs.hasOwnProperty(key)){
            client._.subs[key] = []; 
        }
        client._.subs[key].push(callback);
    },
    unsubscribe: function(key, callback){
        if(client._.subs.hasOwnProperty(key)){
            var index = client._.subs[key].indexOf(callback);
            if(index >= 0){
                client._.subs[key].slice(index, 1);
            }
        }
    },
    once: function(key, callback){
        if(!client._.once.hasOwnProperty(key)){
            client._.once[key] = []; 
        }
        client._.once[key].push(callback);
    },
    ack: function(key, callback){
        if(!client._.ack.hasOwnProperty(key)){
            client._.ack[key] = []; 
        }
        client._.ack[key].push(callback);
    },
    ack_once: function(key, callback){
        if(!client._.ack_once.hasOwnProperty(key)){
            client._.ack_once[key] = []; 
        }
        client._.ack_once[key].push(callback);
    },
    registerInitHook(callback){
        client._.init_hooks.push(callback);
    },
    prepareSend: function(payload, broadcast){
        broadcast = broadcast || false;
        payload.broadcast = broadcast;

        payload.id = client._.id;
        payload.password = client._.password;

        return payload
    },
    send: function(payload, broadcast){
        payload = client.prepareSend(payload, broadcast)
        client.ws.send(JSON.stringify(payload));
    },
    sendBulk: function(payloads, broadcast){
        var prepared_payloads = [];
        for(var payload of payloads){
            prepared_payloads.push(
                client.prepareSend(payload, broadcast));
        }
        client.send({ frames: prepared_payloads, key: "bulk"}, broadcast);
    }
}
