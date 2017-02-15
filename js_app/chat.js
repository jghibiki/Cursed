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

chat.handle_combo = function(){

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
