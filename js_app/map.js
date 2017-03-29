
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


    cursed.client.subscribe("get.map", (data)=>{
        data = data.payload;
        cursed.viewport.updateBounds(data["max_x"], data["max_y"]);
        cursed.viewport.updateFeatures(data["features"]);
    })

    cursed.client.subscribe("get.map.fow", (data)=>{
        cursed.viewport.updateFow(data.payload);
    })

    cursed.client.subscribe("get.map.units", (data)=>{
        cursed.viewport.updateUnits(data.payload);
        if(!cursed.viewer.animation_running){ 
            //prevents a bug where the animation is still 
            //running when the sl is drawn
            cursed.status_line.draw();
        }
    })

    cursed.client.subscribe("list.maps", (data)=>{
        map.maps = data.payload;
        if(map.showing){
            map.show_maps();
        }
    });

    cursed.client.ack("move.user", (data)=>{
        map.load_map();
    });

    cursed.client.subscribe("add.map.unit", (data)=>{
        cursed.viewport.units.push(data.details);

        cursed.viewport.dirty = true;
        cursed.viewport.draw();

        cursed.status_line.dirty = true;
        cursed.status_line.draw();
    });

    cursed.client.subscribe("modify.map.unit", (data)=>{
        var mod_unit = data.details;
        for(var i=0; i<cursed.viewport.units.length; i++){
            var unit = cursed.viewport.units[i];
            if(unit["id"] == mod_unit.id){
                cursed.viewport.units[i] = mod_unit;

                cursed.viewport.dirty = true;
                cursed.viewport.draw();

                cursed.status_line.dirty = true;
                cursed.status_line.draw();
            }
        }
    });

    cursed.client.subscribe("remove.map.unit", (data)=>{
        var unit_id = data.details.id;
        for(var i=0; i<cursed.viewport.units.length; i++){
            var unit = cursed.viewport.units[i];
            if(unit["id"] == unit_id){
                cursed.viewport.units.splice(i, 1);

                cursed.viewport.dirty = true;
                cursed.viewport.draw();

                cursed.status_line.dirty = true;
                cursed.status_line.draw();
            }
        }
    })

    cursed.client.subscribe("modify.map.unit", (data)=>{
        var units = cursed.viewport.units;
        for(var unit of units){
            if(unit.id == data.details.id){
                unit.x = data.details.x;
                unit.y = data.details.y;
                unit.max_health = data.details.max_health;
                unit.current_health = data.details.current_health;
                unit.controller = data.details.controller;
                unit.type = data.details.type;
                unit.name = data.details.name;

                cursed.viewport.dirty = true;
                cursed.viewport.draw();

                cursed.status_line.dirty = true;
                cursed.status_line.draw();
            }
        }
    });

    cursed.client.subscribe("add.map.feature", (data)=>{
        var features = cursed.viewport.features;
        features.push(data.details);
        cursed.viewport.dirty = true;
        cursed.viewport.draw();
    });

    cursed.client.subscribe("remove.map.feature", (data)=>{
        var features = cursed.viewport.features;
        for(feature of features){
            if(feature.x === data.details.x && 
                feature.y === data.details.y){

                var index = features.indexOf(feature);
                cursed.viewport.features.splice(index, 1);

                cursed.viewport.dirty = true;
                cursed.viewport.draw();
                return;
            }
        }
    });

    cursed.client.subscribe("add.map.fow", (data)=>{
        var new_fow = data.details;
        cursed.viewport.fow[new_fow.x][new_fow.y] = true;
        cursed.viewport.dirty = true;
        cursed.viewport.draw();
    });

    cursed.client.subscribe("remove.map.fow", (data)=>{
        var new_fow = data.details;
        cursed.viewport.fow[new_fow.x][new_fow.y] = false;
        cursed.viewport.dirty = true;
        cursed.viewport.draw();
    });

    cursed.client.registerInitHook(()=>{
        map.load_map();
        map.get_maps();
    });
}

map.update = function(hashes){
}

map.handle = function(e){
    if(e.key === "m" && cursed.command_window.mode === cursed.command_window.command_modes.default){
        map.show();
    }
};

map.load_map = function(){

    cursed.client.send({
        type: "command",
        key: "get.map"
    });

    cursed.client.send({
        type: "command",
        key: "get.map.fow"
    });

    cursed.client.send({
        type: "command",
        key: "get.map.units"
    });
}

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

                if(user_to_switch === "*"){
                    var frames = []
                    for(var username of usernames){
                        frames.push({ 
                            type: "command",
                            key: "move.user",
                            details: {
                                username: username,
                                map_name: map_to_switch
                            }
                        });
                    }
                    cursed.client.sendBulk(frames);
                }
                else if(usernames.indexOf(user_to_switch) > -1){
                    cursed.client.send({
                        type: "command",
                        key: "move.user",
                        details: {
                            username: user_to_switch,
                            map_name: map_to_switch
                        }
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
    cursed.client.send({
        type: "command",
        key: "list.maps"
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
