
var users = {};

users.init = function(){
    cursed.modules.interactive.push(users);
    cursed.modules.text_display.push(users);
    cursed.modules.live.push(users);
    users.showing = false;
    users.previous_hash = null;
    users.users = [];
};

users.update = function(hashes){
    
    var hash = hashes["users"];

    if(hash !== users.previous_hash){
        users.previous_hash = hash;
        cursed.client.request("/users", null, (data)=>{
            users.users = data.users;
        });
    }
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

