var map = {
    map_hash: null,
    fow_hash: null,
    unit_hash: null,
    note_hash: null,
    maps: [],
    showing: false,
    loading: {
        features: true,
        types: true,
        units: true,
        fow: true
    }
};

map.init = function(){
    cursed.modules.live.push(map);
    cursed.modules.interactive.push(map);
    cursed.modules.text_display.push(map);


    cursed.client.subscribe("get.map", (data)=>{
        data = data.payload;
        cursed.viewport.updateBounds(data["max_x"], data["max_y"]);
        cursed.viewport.updateFeatures(data["features"]);
        map.loading.features = false;
        if(!map.is_loading()){
            viewport.dirty = true;
            viewport.clear();
            viewport.draw();
        }
    })

    cursed.client.subscribe("get.map.fow", (data)=>{
        cursed.viewport.updateFow(data.payload);
        map.loading.fow = false;
        if(!map.is_loading()){
            viewport.dirty = true;
            viewport.clear();
            viewport.draw();
        }
    })

    cursed.client.subscribe("get.map.units", (data)=>{
        cursed.viewport.updateUnits(data.payload);
        map.loading.units = false;
        if(!cursed.viewer.animation_running){ 
            //prevents a bug where the animation is still 
            //running when the sl is drawn
            cursed.status_line.draw();
            if(!map.is_loading()){
                viewport.dirty = true;
                viewport.clear();
                viewport.draw();
            }
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

        cursed.command_window.dirty = true;
        cursed.command_window.draw();
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

                cursed.command_window.dirty = true;
                cursed.command_window.draw();
                break;
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
    if(cursed.state.role === "gm"){
        if(e.key === "m" && cursed.command_window.mode === cursed.command_window.command_modes.default){
            map.show();
        }
    }
};

map.handle_help = function(buff){

}

map.load_map = function(){

    map.loading = {
        features: true,
        types: true,
        units: true,
        fow: true
    }

    cursed.client.send({
        type: "command",
        key: "get.map.feature.types"
    });

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

    cursed.client.send({
        type: "command",
        key: "get.users"
    });
}

map.handle_combo = function(buff){
    buff = buff.split(" ");
    
    if(buff[0] === "map" || buff[0] === "m" || buff[0] === "maps"){
       
        if(buff.length == 5 && (buff[1] === "add" || buff[1] === "a")){
            var name = buff[2];
            var height = parseInt(buff[3]);
            var width = parseInt(buff[4]);

        }
        else if(buff.length == 4 && (buff[1] === "move" || buff[1] === "m")){
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

        else if (buff.length == 2 && (buff[1] === "features" || buff[1] === "f")){
            var el = $("#features_menu");
            el.dialog({
                resizable: true,
                height: "auto",
                width: "75%",
                modal: true,
                open: function(){
                    // pause keypress handling
                    cursed.viewer.editor_open = true;               
                    $("#features_menu").blur();
                },
                close: function(){
                    // allow client to handle keypresses again
                    cursed.viewer.editor_open = false;               
                },
                buttons: {
                    "Close": function(){
                        $(this).dialog("close");
                    }
                }
            });
        }
        else if(buff.length > 3
            && (buff[1] == "feature" || buff[1] === "f")
            && (buff[2] == "pack" || buff[2] === "p")){
    
            if(buff[3] == "list" || buff[3] == "l"){
                var el = $("#feature_pack_menu");

                var ul = $("#feature_pack_menu_list");

                ul.empty();


                for(var pack of cursed.features.packs){
                    var node = $("<li></li>")
                        .append(
                            $("<p>" + pack.name + "</p>")
                        );

                    var node_ul = $("<ul></ul>");
                    for(var t of pack.types){
                        node_ul.append($("<li/>").text(t.name));
                    }

                    node.append(node_ul);
                    ul.append(node);
                }

                el.dialog({
                    resizable: true,
                    height: "auto",
                    width: "75%",
                    modal: true,
                    open: function(){
                        // pause keypress handling
                        cursed.viewer.editor_open = true;               
                        $("#feature_pack_menu").blur();
                    },
                    close: function(){
                        // allow client to handle keypresses again
                        cursed.viewer.editor_open = false;               
                    },
                    buttons: {
                        "Close": function(){
                            $(this).dialog("close");
                        }
                    }
                });
            }
            else if(buff[3] === "apply" || buff[3] === "a"){

                var pack = null;

                for(var i=0; i<cursed.features.packs.length; i++){
                    if(buff[4].toUpperCase() == cursed.features.packs[i].name.toUpperCase()){
                        pack = cursed.features.packs[i];
                        break;
                    }
                }
                if(pack !== null){
                    
                    var payloads = [];
                    for(var feature_type of pack.types){
                        payloads.push({
                            "type": "command",
                            "key": "add.map.feature.type",
                            "details": feature_type
                        });
                    }

                    cursed.client.sendBulk(payloads, true);
                }
            }
            else if(buff[3] === "remove" || buff[3] === "r"){ /* Remove Feature Pack Types */
                for(var i=0; i<cursed.features.packs.length; i++){
                    if(buff[4].toUpperCase() == cursed.features.packs[i].name.toUpperCase()){
                        pack = cursed.features.packs[i];
                        break;
                    }
                }
                if(pack !== null){
                    var payloads = [];
                    for(var feature_type of pack.types){
                        payloads.push({
                            "type": "command",
                            "key": "remove.map.feature.type",
                            "details": {
                                "name": feature_type.name
                            }
                        });
                    }

                    cursed.client.sendBulk(payloads, true);
                }
            }
        }
        else if(buff.length === 4
            && (buff[1] === "feature" || buff[1] === "f")
            && (buff[2] === "rm" || buff[2] === "r")){
            for(var feature of features.objects){
                if(feature.name === buff[3]){
                    cursed.client.send({
                        type: "command",
                        key: "remove.map.feature.type",
                        details:{
                            "name": name
                        }
                    }, true);
                    
                    break;
                }
            }
        }
        else if(buff.length === 3 
            && (buff[1] === "feature" || buff[1] === "f")
            && (buff[2] === "add" || buff[2] === "a")){

            var el = $("#features_add_menu");
            el.dialog({
                resizable: true,
                height: "auto",
                width: "auto",
                modal: true,
                open: function(){
                    // pause keypress handling
                    cursed.viewer.editor_open = true;               
                    $("#features_add_menu").blur();
                },
                close: function(){
                    // allow client to handle keypresses again
                    cursed.viewer.editor_open = false;               
                },
                buttons: {
                    "Add": function(){

                        var feature_name = $("#feature_name");
                        name = feature_name.val();
                        if(name === "" || name === null || name === undefined){
                            return;
                        }

                        var feature_key = $("#feature_key");
                        key = feature_key.val();
                        if(key === "" || key === null || key === undefined){
                            return;
                        }

                        var feature_character = $("#feature_character");
                        character = feature_character.val();
                        if(character === "" || character === null || character === undefined){
                            return;
                        }

                        var feature_color = $("#feature_color");
                        color = feature_color.val();
                        if(color === "" || color === null || color === undefined){
                            return;
                        }

                        cursed.client.send({
                            type: "command",
                            key: "add.map.feature.type",
                            details:{
                                "name": name,
                                "key": key,
                                "character": character,
                                "color": color
                            }
                        }, true);

                        $(this).dialog("close");
                    },
                    "Close": function(){
                        $(this).dialog("close");
                    }
                }
            });
              
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

map.is_loading = function(){
    return (
        map.loading.fow ||
        map.loading.features ||
        map.loading.types ||
        map.loading.units );
}
