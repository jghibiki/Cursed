"use strict";

var viewport = {};

viewport.init = function(){

    cursed.modules.interactive.push(viewport);
    
    viewport.x = 0 
    viewport.y = 0;
    viewport.width = Math.ceil(cursed.constants.grid_width/2);
    viewport.height = cursed.constants.grid_height-3;

    viewport.cursor_x = 10;
    viewport.cursor_y = 10;

    // virtual width and height. should be set to map h and w
    viewport.v_x = 0;
    viewport.v_y = 0;
    viewport.v_height = viewport.height;
    viewport.v_width = viewport.width; 

    viewport.features = [];
    viewport.fow = [];

    viewport.dirty = true;

    var diff = new Array(cursed.grid._.length);
    for(var i=0; i<cursed.grid._.length; i++){
        diff[i] = new Array(cursed.grid._[0].length);
        for(var j=0; j<cursed.grid._[0].length; j++){
            diff[i][j] = null;
        }
    }
    viewport.last = diff

    viewport.clear();
}

viewport.draw = function(){

    if(viewport.dirty){

        var diff = new Array(cursed.grid._.length);
        for(var i=0; i<cursed.grid._.length; i++){
            diff[i] = new Array(cursed.grid._[0].length);
            for(var j=0; j<cursed.grid._[0].length; j++){
                diff[i][j] = null;
            }
        }

        var keys = Object.keys(viewport.features);
        var len = keys.length;
        var i = 0;

        while(i < len){
            var feature = viewport.features[keys[i]];
            if(feature.x >= viewport.v_x && 
               feature.y >= viewport.v_y &&
               feature.x < (viewport.v_x + viewport.width) &&
               feature.y < (viewport.v_y + viewport.height) &&
               ( cursed.state.fow == "off" || 
                   ( viewport.fow[feature.x] !== undefined && !viewport.fow[feature.x][feature.y] )
               )){

                var raw_feature = cursed.features.get(feature.type);
                if(raw_feature !== null && raw_feature !== undefined){
                    var character = raw_feature.character;
                    if(character !== null && character !== undefined){
                        diff[feature.y - viewport.v_y][feature.x - viewport.v_x] = feature.type;
                        cursed.grid.text(feature.y - viewport.v_y, feature.x - viewport.v_x, character, raw_feature.color);
                    }
                }
            }

            i++;
        }


        if(cursed.state.fow == "on"){
            for(var x=0; x<viewport.fow.length; x++){
                for(var y=0; y<viewport.fow[x].length; y++){
                    if(viewport.fow[x][y] &&
                       x >= viewport.v_x && 
                       y >= viewport.v_y &&
                       x < (viewport.v_x + viewport.width) &&
                       y < (viewport.v_y + viewport.height)){

                        diff[y - viewport.v_y][x - viewport.v_x] = "FOW";;
                        cursed.grid.text(y - viewport.v_y, x - viewport.v_x, "\u2588", "Light Grey");
                    }
                }
            }
        }

        //clear blocks not in new rendering
        for(var i=0; i<diff.length; i++){
            for(var j=0; j<diff[i].length; j++){
                if( viewport.last[i][j] === diff[i][j] ){
                    cursed.grid.text(viewport.y + i, viewport.x + j, " ", "Gold");
                }
            }
        }

        // Draw Cursor
        cursed.grid.text(viewport.y + viewport.cursor_y, viewport.x + viewport.cursor_x, "X", "Gold");

        viewport.dirty = false;
        cursed.viewer.dirty = true;
    }
    
};

viewport.clear = function(){
    for(var y=0; y<viewport.height; y++){
        for(var x=0; x<viewport.width; x++){
            //cursed.grid.text(viewport.y + y, viewport.x + x, " ", "Gold");
        }
    }
}


viewport.handle = function(event){
    if(event.key === "j"){ viewport.cursor_down(); }
    if(event.key === "k"){ viewport.cursor_up(); }
    if(event.key === "h"){ viewport.cursor_left(); }
    if(event.key === "l"){ viewport.cursor_right(); }

    if(event.key === "J"){ viewport.down(); }
    if(event.key === "K"){ viewport.up(); }
    if(event.key === "H"){ viewport.left(); }
    if(event.key === "L"){ viewport.right(); }
}

viewport.handle_combo = function(event){};

viewport.cursor_up = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 100);

    if(viewport.cursor_y > 0){
        cursed.grid.text(viewport.y + viewport.cursor_y, viewport.x + viewport.cursor_x, " ", "Gold");
        viewport.cursor_y -= 1;
        viewport.dirty = true;

        viewport.draw();
    }
}

viewport.cursor_down = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 100);

    if(viewport.cursor_y < viewport.v_height-1){
        cursed.grid.text(viewport.y + viewport.cursor_y, viewport.x + viewport.cursor_x, " ", "Gold");
        viewport.cursor_y += 1;
        viewport.dirty = true;

        viewport.draw();
    }
}

viewport.cursor_left = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 100);

    if(viewport.cursor_x > 0){
        cursed.grid.text(viewport.y + viewport.cursor_y, viewport.x + viewport.cursor_x, " ", "Gold");
        viewport.cursor_x -= 1;
        viewport.dirty = true;

        viewport.draw();
    }
}

viewport.cursor_right = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 100);

    if(viewport.cursor_x < viewport.v_width-1){
        cursed.grid.text(viewport.y + viewport.cursor_y, viewport.x + viewport.cursor_x, " ", "Gold");
        viewport.cursor_x += 1;
        viewport.dirty = true;

        viewport.draw();

    }
}

viewport.up = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 100);

    if(viewport.v_y > 2){
        viewport.v_y -= 2;
        viewport.dirty = true;
        viewport.clear();
        viewport.draw();
    }
    else if(viewport.v_y > 0){
        viewport.v_y -= 1;
        viewport.dirty = true;
        viewport.clear();
        viewport.draw();
    }
}

viewport.down = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 100);

    if(viewport.v_y < ((viewport.v_height - viewport.height) - 2)){
        viewport.v_y += 2;
        viewport.dirty = true;
        viewport.clear();
        viewport.draw();
    }
    else if(viewport.v_y < ((viewport.v_height - viewport.height) - 1)){
        viewport.v_y += 1;
        viewport.dirty = true;
        viewport.clear();
        viewport.draw();
    }
}

viewport.left = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 100);

    if(viewport.v_x > 2){
        viewport.v_x -= 2;
        viewport.dirty = true;
        viewport.clear();
        viewport.draw();
    }
    else if(viewport.v_x > 0){
        viewport.v_x -= 1;
        viewport.dirty = true;
        viewport.clear();
        viewport.draw();
    }
}

viewport.right = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 100);

    if(viewport.v_x < ((viewport.v_width - viewport.width) - 2)){
        viewport.v_x += 2;
        viewport.dirty = true;
        viewport.clear();
        viewport.draw();
    }
    else if(viewport.v_x < ((viewport.v_width - viewport.width) - 1)){
        viewport.v_x += 1;
        viewport.dirty = true;
        viewport.clear();
        viewport.draw();
    }
}


viewport.updateBounds = function(y, x){
    viewport.v_height = y;
    viewport.v_width = x;
}

viewport.updateFeatures = function(features){
    viewport.features = features;
    viewport.dirty = true;
    viewport.clear();
    viewport.draw();
}

viewport.updateFow = function(fow){
    viewport.fow = fow;
    viewport.dirty = true;
    viewport.clear();
    viewport.draw();
}
