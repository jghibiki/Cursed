
var users = {};

users.init = function(){
    cursed.modules.interactive.push(users);
    cursed.modules.text_display.push(users);
    cursed.modules.live.push(users);
    users.showing = false;
    users.previous_hash = null;
    users.users = [];

    cursed.client.subscribe("get.users", (data)=>{
        users.users = data.payload;
        if(cursed.map.showing){
            cursed.map.show();
        }
    });

    cursed.client.registerInitHook(()=>{
        cursed.client.once("get.users", (data)=>{
            for(var user of data.payload){
                if(user.username == cursed.state.username){
                    cursed.state.role = user.role;
                    // update command window based on role, but not if animation is still running
                    if(!cursed.viewer.animation_running){
                        cursed.command_window.dirty = true;
                        cursed.command_window.draw();
                    }
                }
            }
        });
        cursed.client.send({
            type: "command",
            key: "get.users"
        });

    });
};

users.update = function(hashes){
};

users.handle = function(){
    //TODO: implement users.handle
};

users.handle_combo = function(){
    //TODO: implement users.handle_combo
};

users.handle_help = function(){
    //TODO: implement users.handle_help
};

users.show = function(){
    //TODO: implement users.show
}

users.hide = function(){
    //TODO: implement users.hide
};

