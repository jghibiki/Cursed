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
    viewport.units = [];

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

        // Draw features
        while(i < len){
            var feature = viewport.features[keys[i]];
            if(feature.x >= viewport.v_x &&  /* feature is within visible bounds */
               feature.y >= viewport.v_y &&
               feature.x < (viewport.v_x + viewport.width) &&
               feature.y < (viewport.v_y + viewport.height) &&
               ( cursed.state.fow == "off" ||  /* fog of war is not off and not occluding feature */
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

        // Draw units
        for(var i=0; i<viewport.units.length; i++){
            var unit = viewport.units[i];

            if(unit.x >= viewport.v_x && /* unit is within visible bounds */
               unit.y >= viewport.v_y &&
               unit.x < (viewport.v_x + viewport.width) &&
               unit.y < (viewport.v_y + viewport.height) &&
               ( cursed.state.fow == "off" ||  /* fog of war is not off and not occluding unit */
                   ( viewport.fow[unit.x] !== undefined && !viewport.fow[unit.x][unit.y] )
                )){

                var corrected_y = unit.y - viewport.v_y;
                var corrected_x = unit.x - viewport.v_x;
                diff[corrected_y][corrected_x] = "unit:" + unit.id;
                if(unit.controller == cursed.state.username  && cursed.state.role != "gm"){
                    cursed.grid.text(corrected_y, corrected_x, "@", "Light Blue");
                }
                else if(unit.type == "pc"){
                    cursed.grid.text(corrected_y, corrected_x, "@", "Light Green");
                }
                else if(unit.type == "enemy"){
                    cursed.grid.text(corrected_y, corrected_x, "@", "Light Red");
                }
                else if(unit.type == "neutral"){
                    cursed.grid.text(corrected_y, corrected_x, "@", "Light Grey");
                }
            }
        }


        // Draw fog of war
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
    if(!cursed.viewer.handling){
        if(event.key === "j"){ viewport.cursor_down(); }
        else if(event.key === "k"){ viewport.cursor_up(); }
        else if(event.key === "h"){ viewport.cursor_left(); }
        else if(event.key === "l"){ viewport.cursor_right(); }

        else if(event.key === "J"){ viewport.down(); }
        else if(event.key === "K"){ viewport.up(); }
        else if(event.key === "H"){ viewport.left(); }
        else if(event.key === "L"){ viewport.right(); }
    }
        
    if(event.key == "f"){
        if(cursed.state.fow === "on"){
            cursed.state.fow = "off";
            cursed.viewport.dirty = true;
            cursed.viewport.clear();
            cursed.viewport.draw();
        }
        else if(cursed.state.fow == "off"){
            cursed.state.fow = "on";
            cursed.viewport.dirty = true;
            cursed.viewport.clear();
            cursed.viewport.draw();
        }
    }
    else if (event.key === "+" || event.key === "="){
        var unit = viewport.getCurrentUnit();
        
        if(unit !== null){
            unit.current_health += 1

            cursed.client.request("/unit/update", unit, null);
        }
    }
    else if (event.key === "-"){
        var unit = viewport.getCurrentUnit();
        
        if(unit !== null){
            unit.current_health -= 1

            cursed.client.request("/unit/update", unit, null);
        }
    }
}

viewport.handle_combo = function(event){};

viewport.cursor_up = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 200);

    if(viewport.cursor_y > 0){
        cursed.grid.text(viewport.y + viewport.cursor_y, viewport.x + viewport.cursor_x, " ", "Gold");
        viewport.cursor_y -= 1;
        viewport.dirty = true;

        viewport.draw();

        cursed.status_line.draw();
    }
}

viewport.cursor_down = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 200);

    if(viewport.cursor_y < viewport.v_height-1){
        cursed.grid.text(viewport.y + viewport.cursor_y, viewport.x + viewport.cursor_x, " ", "Gold");
        viewport.cursor_y += 1;
        viewport.dirty = true;

        viewport.draw();

        cursed.status_line.draw();
    }
}

viewport.cursor_left = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 200);

    if(viewport.cursor_x > 0){
        cursed.grid.text(viewport.y + viewport.cursor_y, viewport.x + viewport.cursor_x, " ", "Gold");
        viewport.cursor_x -= 1;
        viewport.dirty = true;

        viewport.draw();

        cursed.status_line.draw();
    }
}

viewport.cursor_right = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 200);

    if(viewport.cursor_x < viewport.v_width-1){
        cursed.grid.text(viewport.y + viewport.cursor_y, viewport.x + viewport.cursor_x, " ", "Gold");
        viewport.cursor_x += 1;
        viewport.dirty = true;

        viewport.draw();

        cursed.status_line.draw();
    }
}

viewport.up = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 200);

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

    cursed.status_line.draw();
}

viewport.down = function(){
    cursed.viewer.handling = true;
    setTimeout(()=>{cursed.viewer.handling = false;}, 200);

    if(viewport.v_y < ((viewport.v_height - viewport.height) - 2)){
        viewport.v_y += 2;
        viewport.dirty = true;
        viewport.clear();
        viewport.draw();
        cursed.status_line.draw();
    }
    else if(viewport.v_y < ((viewport.v_height - viewport.height) - 1)){
        viewport.v_y += 1;
        viewport.dirty = true;
        viewport.clear();
        viewport.draw();
        cursed.status_line.draw();
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
        cursed.status_line.draw();
    }
    else if(viewport.v_x > 0){
        viewport.v_x -= 1;
        viewport.dirty = true;
        viewport.clear();
        viewport.draw();
        cursed.status_line.draw();
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
        cursed.status_line.draw();
    }
    else if(viewport.v_x < ((viewport.v_width - viewport.width) - 1)){
        viewport.v_x += 1;
        viewport.dirty = true;
        viewport.clear();
        viewport.draw();
        cursed.status_line.draw();
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

viewport.updateUnits = function(units){
    viewport.units = units;
    viewport.dirty = true;
    viewport.clear();
    viewport.draw();
};

viewport.getCursorFocus = function(){
    var unit = null;
    var feature = null;

    var i = viewport.units.length;
    while(i--){
        var u = viewport.units[i];
        if(u.x == viewport.cursor_x &&
           u.y == viewport.cursor_y){
            unit = u;
            break;
        }
    }

    if (unit === null){
        var i = viewport.features.length;
        // Draw features
        while(i--){
            var f = viewport.features[i];
            if(f.x == viewport.cursor_x &&
               f.y == viewport.cursor_y){
                feature = f;
                break;
            }
        }
    }

    if( !(  cursed.state.role === "pc" && viewport.fow[viewport.cursor_y] !== undefined && viewport.fow[viewport.cursor_y][viewport.cursor_x] )){
        
        if(unit !== null){
            var text = unit.name + " " + unit.current_health + "/" + unit.max_health;
            var bar = "";
            
            if(unit.max_health !== 0){
                var font_width = cursed.constants.font_size + cursed.constants.font_width_offset;
                var width = Math.floor((cursed.colon_line.width- (12 + (4+text.length)*font_width))/(font_width));

                var percent = unit.current_health/(unit.max_health*1.0);

                if(percent <= 1.0 && percent >= 0.0){
                    var number_of_units =  Math.ceil(width*percent);
                    bar = Array(number_of_units+1).join("=");
                    var width_padding = Array(width).join(" ");
                    bar = String(width_padding + bar).slice(-width);
                }
                else if(percent > 1.0){
                    var diff = percent - 1.0;
                    var diff_percent = diff/percent;
                    var excess = Math.ceil(width * diff_percent);

                    bar = Array(excess+1).join("=");
                    bar += "(+)|";

                    var width_padding = Array(width+1).join("=");
                    bar = String(bar + width_padding ).substring(0, width);
                }
                else if(percent < 0.0){
                    var diff = (-1 * percent)/(1.0 + (-1 * percent));
                    var excess = Math.ceil(width * diff);

                    bar = "|(-)"
                    bar += Array(excess+1).join("=");

                    var width_padding = Array(width).join(" ");
                    bar = String(width_padding + bar).slice(-width);
                }

            }

            return text + " [" + bar + "]";
        }
        else if (feature !== null){
            var text = feature.type;
            return text;
        }
        else{
            return "";
        }

    }
}

viewport.getCurrentUnit = function(){
    var i = viewport.units.length;
    while(i--){
        var u = viewport.units[i];
        if(u.x === viewport.cursor_x && u.y === viewport.cursor_y){
            return u;
        }
    }
    return null;
}
