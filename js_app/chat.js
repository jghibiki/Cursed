"use strict";

var chat = {};

chat.init = function(){
    cursed.modules.interactive.push(chat);
    cursed.modules.text_display.push(chat);
    cursed.modules.live.push(chat);
    chat.showing = false;
    chat.previous_hash = null;
    chat.messages = [];
};

chat.update = function(hashes){
    var hash = hashes["chat"];

    if(hash !== chat.previous_hash){
        chat.previous_hash = hash;

        cursed.client.request("/chat/"+cursed.state.username, null, cursed.chat.get_messages);
    }
};

chat.handle = function(e){
    if(e.key === "c"){
        chat.show();        
    }
};

chat.handle_combo = function(buff){
    buff = buff.split(" ");
    if( ( buff[0] === "chat" || buff[0] === "c" ) && buff.length > 1){
        var data = {
            sender: cursed.state.username,
            recipient: null,
            message: buff.slice(1).join(" "),
            persona: null
        };
        cursed.client.request("/chat", data, ()=>{
            chat.get_messages();
        });
        chat.show();

    }
    else if( (buff[0] === "whisper" || buff[0] === "w") && buff.length > 2){
        var data = {
            sender: cursed.state.username,
            recipient: buff[1],
            message: buff.slice(2).join(" "),
            persona: null
        };
        cursed.client.request("/chat", data, ()=>{
            chat.get_messages();
            chat.show();
        });
    }
    else if( (buff[0] === "impersonate" || buff[0] === "imp") && buff.length > 2){
        var data = {
            sender: cursed.state.username,
            recipient: null,
            message: buff.slice(2).join(" "),
            persona: buff[1]
        };
        cursed.client.request("/chat", data, ()=>{
            chat.get_messages();
            chat.show();
        });
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

chat.get_messages = function(data){

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

    if(!data.hasOwnProperty("messages")){return;}
    for(var message of data.messages){
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
