
var map = {
    map_hash: null,
    fow_hash: null,
    unit_hash: null,
    note_hash: null,
    maps: [],
    showing: false
};

map.init = function(){
    cursed.modules.live.push(map);
    cursed.modules.interactive.push(map);
    cursed.modules.text_display.push(map);

    map.get_maps();
}

map.update = function(hashes){
    var update = false;

    var map_hash = hashes["map"]
    if(map_hash !== map.map_hash){
        map.map_hash = map_hash;
        
        cursed.client.request("/map/data/", null, (data)=>{
            cursed.viewport.updateBounds(data["max_x"], data["max_y"]);
            cursed.viewport.updateFeatures(data["features"]);
        });
    }

    var fow_hash = hashes["fow"];
    if(fow_hash !== map.fow_hash){
        map.fow_hash = fow_hash;

        cursed.client.request("/fow", null, (data)=>{
            cursed.viewport.updateFow(data["fow"]);
        });

    }

    var unit_hash = hashes["units"];
    if(unit_hash !== map.unit_hash){
        map.unit_hash = unit_hash;

        cursed.client.request("/unit", null, (data)=>{
            cursed.viewport.updateUnits(data["units"]);
            if(!cursed.viewer.animation_running){ //prevents a bug where the animation is still running when the sl is drawn
                cursed.status_line.draw();
            }
        });
    }
}

map.handle = function(e){
    if(e.key === "m" && cursed.command_window.mode === cursed.command_window.command_modes.default){
        map.show();
    }
};

map.handle_combo = function(buff){
    buff = buff.split(" ");
    
    if(buff[0] === "map" || buff[0] === "m" || buff[0] === "maps"){

        if(buff.length == 4 && (buff[1] === "move" || buff[1] === "m")){
            user_to_switch = buff[2];
            map_to_switch = buff[3];

            var valid_map = false;
            for(var map_name of map.maps){
                if(map_name == map_to_switch){
                    valid_map = true;
                    break
                }
            }
            
            if(valid_map){
                usernames = cursed.users.users.map((user)=>{
                    return user.username;
                });

                if(usernames.indexOf(user_to_switch) > -1){
                    cursed.client.request("/map", {
                        username: user_to_switch,
                        map_name: map_to_switch
                    });
                }
            }
        }
    }
}

map.show = function(){
    cursed.modules.text_display.map((e)=>{e.hide()});
    map.showing = true;
    map.get_maps()
    map.show_maps()
}

map.hide = function(){
    map.showing = false;
}

map.get_maps = function(){
    cursed. client.request("/map", null, (data)=>{
        map.maps = data.maps.sort();
        if(map.showing){
            map.show_maps();
        }
    });
};

map.show_maps = function(){
    lines = [ [{
        text: "Maps",
        color: "Gold"
    }] ];

    for(var map_name of map.maps){
        lines.push([{
            text: map_name,
            color: "Light Blue"
        }]);

        for(var user of cursed.users.users){
            if(user.current_map === map_name){
                lines.push([{
                    text: "- " + user.username,
                    color: null
                }]);
            }
        }
    }

    cursed.text_box.set(lines);
}
