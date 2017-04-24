"use strict";

var features = {
    
};

features.objects = [];


features.init = function(){
    cursed.client.subscribe("get.map.feature.types", (data)=>{
        features.objects = data.payload;
        cursed.map.loading.types  = false;
        if(!cursed.map.is_loading()){
            viewport.dirty = true;
            viewport.clear();
            viewport.draw();
        }
    });

    cursed.client.subscribe("add.map.feature.type", (data)=>{
        features.objects.push(data.details);
        cursed.client.send({
            type: "command",
            key: "get.map"
        });

        /* update command window if build menu is showing */
        if(cursed.command_window.mode === cursed.command_window.command_modes.build){
            cursed.command_window.dirty = true;
            cursed.command_window.draw();
        }
    });

    cursed.client.subscribe("remove.map.feature.type", (data)=>{
        for(var i=0; i<features.objects.length; i++){
            if(features.objects[i].name == data.details.name){
                features.objects.splice(i, 1);
                break;
            }
        }

        /* update command window if build menu is showing */
        if(cursed.command_window.mode === cursed.command_window.command_modes.build){
            cursed.command_window.dirty = true;
            cursed.command_window.draw();
        }

        /* reload the map when a feature type is removed because all related features
         * are pruned from the map
         */
        cursed.client.send({
            type: "command",
            key: "get.map"
        });
    });

    cursed.client.registerInitHook(()=>{
        cursed.client.send({
            type: "command",
            key: "get.map.feature.types"
        });
    });

    cursed.modules.interactive.push(features);
}

features.handle = function(e){
}

features.handle_combo = function(buff){
}

features.handle_help = function(buff){

}

features.test = function(){
    var x = 0;
    var y = 0;
    var texts = [];

    var max = 20;

    for(let feature of features.objects){
        var text = new createjs.Text(feature.character, "20px monospace", feature.color.value);
        var h =  text.getMeasuredHeight();
        if(h > max){ max = h; }
        texts.push(text);
    }

    for(let text of texts){
        text.x = x;
        text.y = y;
        stage.addChild(text);
        y = y + max;
    }
    stage.update();
}



features.new = function(feature_name, x, y){
    var new_feature = null;
    for(feature of feature.objects){
        if(feature.name == feature_name){
            new_feature = feature;
        }
    }

    if(new_feature !== null){
        var text = new createjs.Text(new_feature.character, "20px monospace", new_feature.color.value);
        text.x = x;
        text.y = y;
        return text;
    }
    return null;
}

features.get = function(name){
    for(var feature of features.objects){
        if(feature.name == name){
            return feature;
        }
    }
    return {
        "name": "Missing Feature Type: " + name,
        "character": "?", 
        "color": "Red"
    }

}

features.packs = [
    { 
        name: "Fantasy",
        types: [
            { "name": "Wall",       "character": "\u2588",  "color": "Brown",       "key": "w" },
            { "name": "Table",      "character": "T",       "color": "Brown",       "key": "T" },
            { "name": "Chair",      "character": "c",       "color": "Brown",       "key": "c" },
            { "name": "Door",       "character": "d",       "color": "Brown",       "key": "d" },
            { "name": "Up Stair",   "character": "\u2191",  "color": "Brown",       "key":">" },
            { "name": "Down Stair", "character": "\u2193",  "color": "Brown",       "key": "<" },
            { "name": "Lantern",    "character": "%",       "color": "Gold",        "key": "%" },
            { "name": "Road",       "character": "\u2588",  "color": "Grey",        "key": "r" },
            { "name": "Chest",      "character": "#",       "color": "White",       "key": "#" },
            { "name": "Gate",       "character": "G",       "color": "Brown",       "key": "G" },
            { "name": "Water",      "character": "~",       "color": "Light Blue",  "key": "~" },
            { "name": "Tree",       "character": "O",       "color": "Brown",       "key": "t" },
            { "name": "Bush",       "character": "o",       "color": "Dark Green",  "key":"o" },
            { "name": "Grass",      "character": ".",       "color": "Dark Green",  "key": "." },
            { "name": "Hill",       "character": "^",       "color": "White",       "key": "^" },
            { "name": "Bed",        "character": "b",       "color": "Brown",       "key": "b" },
            { "name": "Statue",     "character": "&",       "color": "White",       "key":"&" },
            { "name": "Blood",      "character": "\u2588",  "color": "Dark Red",    "key":"B" },
            { "name": "Fire",       "character": "~",       "color": "Orange",      "key": "f"},
            { "name": "Snow",       "character": "\u2588",  "color": "White",       "key":"s" },
            { "name": "Boulder",    "character": "O",       "color": "Dark Grey",   "key": "O"}
        ]
    },
    {
        name: "test",
        types: [
            { "name": "Test", "character": "J", "color": "Gold", "key": "z" }
        ]
    }
];
