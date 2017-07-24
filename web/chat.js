"use strict";

var chat = {
    raw_messages: [],
    messages: []
};

chat.init = function(){
    cursed.modules.interactive.push(chat);
    cursed.modules.text_display.push(chat);
    cursed.modules.live.push(chat);
    chat.showing = false;
    chat.previous_hash = null;
    chat.messages = [];

    cursed.client.subscribe("get.chat", (data)=>{
        chat.raw_messages = data.payload
        chat.build_lines(chat.raw_messages);        
    });

    cursed.client.subscribe("add.chat.message", (data)=>{
        chat.raw_messages.push(data.details);
        chat.build_lines(chat.raw_messages);        
    });

    cursed.client.subscribe("clear.chat", (data)=>{
        chat.raw_messages = [];
        chat.build_lines(chat.raw_messages);
    });

    cursed.client.registerInitHook(()=>{
        cursed.client.send({
            type: "command",
            key: "get.chat"
        });
    });

};

chat.update = function(hashes){
};

chat.handle_help = function(buff){

}

chat.handle = function(e){
    if(command_window.mode === command_window.command_modes.default){
        if(e.key === "c"){
            chat.show();        
        }
    }
};

chat.handle_combo = function(buff){
    buff = buff.split(" ");
    if( ( buff[0] === "chat" || buff[0] === "c" ) && buff.length > 1){
        if(buff[1] === "clear"){
            cursed.client.send({
                type: "command",
                key: "clear.chat"
            }, true);
        }
        else{
            var data = {
                sender: cursed.state.username,
                recipient: null,
                message: buff.slice(1).join(" "),
                persona: null
            };
            cursed.client.send({
                type: "command",
                key: "add.chat.message",
                details: data
            }, true);
            chat.show();
        }
    }
    else if( (buff[0] === "whisper" || buff[0] === "w") && buff.length > 2){
        var data = {
            sender: cursed.state.username,
            recipient: buff[1],
            message: buff.slice(2).join(" "),
            persona: null
        };
        cursed.client.send({
            type: "command",
            key: "add.chat.message",
            details: data
        }, true);
        chat.show();
    }
    else if( (buff[0] === "impersonate" || buff[0] === "imp") && buff.length > 2){
        var data = {
            sender: cursed.state.username,
            recipient: null,
            message: buff.slice(2).join(" "),
            persona: buff[1]
        };
        cursed.client.send({
            type: "command",
            key: "add.chat.message",
            details: data
        }, true);
        chat.show();
    }
};

chat.show = function(){
    // hide all modules
    cursed.modules.text_display.map((e)=>{e.hide();});
    //show chat
    chat.showing = true;
    cursed.text_box.set(chat.messages);
};

chat.hide = function(){
    chat.showing = false;
};

chat.build_lines = function(data){

    var gm_user = null;
    for(var user of cursed.users.users){
        if(user.role == "gm"){
            gm_user = user.username;
            break;
        }
    }

    var lines = [ [{
        text: "Chat:",
        color: "Gold"
    }] ];

    for(var message of data){
        if(message.recipient !== null){
            var line = [ {
                text: "<private> " + message.sender + " to " + message.recipient + ":",
                color: "Dark Green"
            },{
                text: message.message,
                color: null
            }];
        }
        else if (message.persona !== null){
            if(message.sender === gm_user){
                var line = [
                    {
                        text: message.persona + " <" + message.sender + ">:",
                        color: "Gold"
                    }, {
                        text: message.message,
                        color: null
                    }
                ];
            }
            else{
                var line = [
                    {
                        text: message.persona + " <" + message.sender + ">:",
                        color: "Grey"
                    }, {
                        text: message.message,
                        color: null
                    }
                ]
            }
        }
        else {
            if(message.sender === gm_user){
                var line = [
                    {
                        text: message.sender + ":",
                        color: "Gold"
                    }, {
                        text: message.message,
                        color: null
                    }
                ];
            }
            else{
                var line = [
                    {
                        text: message.sender + ":",
                        color: "Grey"
                    }, {
                        text: message.message,
                        color: null
                    }
                ];
            }
        }
        lines.push(line);
    }

    chat.messages = lines;

    if(chat.showing){
        cursed.text_box.set(lines);
    }
};
