"use strict";


var command_window = {
    mode: 0,
    first_draw: true,
    command_modes: {
        default: 0,
        build: 1,
        fow: 2,
        units: 3,
        unit_move: 4,
        box_select: 5
    },
    box: false,
    dirty: true
};

command_window.types = {
    interactive: true
};

command_window.init = function(){

    command_window.y = 0;
    command_window.x = Math.ceil((cursed.constants.width/3) + (cursed.constants.width/2) + 1);

    command_window.width = Math.floor(cursed.constants.width - command_window.x - 1);
    var height = cursed.constants.height - (3 * cursed.constants.font_size);
    var correction = height % cursed.constants.font_size;
    command_window.height = height - correction;

    command_window.cont = new createjs.Container();
    command_window.cont.x = command_window.x + cursed.constants.font_size;
    command_window.cont.y = command_window.y+20;
    command_window.cont.cache(0, 0, command_window.width*2, command_window.height*2);
    cursed.stage.addChild(command_window.cont);

    cursed.modules.interactive.push(command_window);
};
command_window.draw = function(){
    
    if(command_window.dirty){
        if(command_window.first_draw){
            /* Top Box */
            (function(){
                var box = new createjs.Shape();
                box.graphics.append(createjs.Graphics.beginCmd);

                box.graphics.append(new createjs.Graphics.Rect(command_window.x, command_window.y, command_window.width, cursed.constants.font_size));
                
                box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

                cursed.stage.addChild(box);
            })();

            /* Bottom Box */
            (function(){
                var box = new createjs.Shape();
                box.graphics.append(createjs.Graphics.beginCmd);

                box.graphics.append(new createjs.Graphics.Rect(command_window.x, command_window.y + (command_window.height-cursed.constants.font_size), command_window.width, cursed.constants.font_size));
                
                box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

                cursed.stage.addChild(box);
            })();

            /* Left Box */
            (function(){
                var box = new createjs.Shape();
                box.graphics.append(createjs.Graphics.beginCmd);

                box.graphics.append(new createjs.Graphics.Rect(command_window.x, command_window.y, cursed.constants.font_size + cursed.constants.font_width_offset, command_window.height));
                
                box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

                cursed.stage.addChild(box);
            })();

            /* Right Box */
            (function(){
                var box = new createjs.Shape();
                box.graphics.append(createjs.Graphics.beginCmd);

                box.graphics.append(
                    new createjs.Graphics.Rect(
                        command_window.x + (command_window.width - (cursed.constants.font_size + cursed.constants.font_width_offset)), 
                        command_window.y, 
                        cursed.constants.font_size + cursed.constants.font_width_offset, 
                        command_window.height));
                
                box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

                cursed.stage.addChild(box);
            })();
            
            command_window.first_draw = true;
        }
    command_window.cont.removeAllChildren();
        if(command_window.mode === command_window.command_modes.default){
            if(cursed.state.role === "pc"){
                command_window.draw_pc_default_screen();
            }
            else if(cursed.state.role === "gm"){
                command_window.draw_gm_default_screen();
            }
        }

        if(command_window.mode === command_window.command_modes.build){
            command_window.draw_build_screen();
        }

        command_window.dirty = false;
        cursed.viewer.dirty = true;
    }
}

command_window.draw_title = function(line_no, text){
    var offset_width = Math.floor(command_window.width/(cursed.constants.font_size + cursed.constants.font_width_offset))-3;
    var split_text = text.match(new RegExp('.{1,' + offset_width + '}', "g"));
    var color_obj = cursed.colors.get("Gold");
    for(var t of split_text){

        //creating and positioning
        var text_obj = new createjs.BitmapText(t, cursed.ss);
        text_obj.x = 0;
        text_obj.y = cursed.constants.font_size * line_no;
        text_obj.letterSpacing = cursed.constants.font_spacing;

        //setting color
        text_obj.filters = [
            new createjs.ColorFilter(0, 0, 0, 1, color_obj.r, color_obj.g, color_obj.b, 0)
        ];

        //caching and adding to cont
        var bounds = text_obj.getBounds();
        var w = bounds.width;
        var h = bounds.height;
        command_window.cont.addChild(text_obj);
        text_obj.cache(0, 0, w*2, h*2);

        line_no += 1;
    }
    command_window.cont.updateCache();
    return line_no;
}

command_window.draw_key = function(line_no, ch, text){
    var offset_width = Math.floor(command_window.width/(cursed.constants.font_size + cursed.constants.font_width_offset))-3;

    
    var split_text = text.match(new RegExp('.{1,' + offset_width + '}', "g"));
    var gold = cursed.colors.get("Gold");
    var white = cursed.colors.get("White");

    var ch_no = 0;
    
    // Adding character text
    //creating and positioning
    var text_obj = new createjs.BitmapText(ch, cursed.ss);
    text_obj.x = 0;
    text_obj.y = cursed.constants.font_size * line_no;
    text_obj.letterSpacing = cursed.constants.font_spacing;

    //setting color
    text_obj.filters = [
        new createjs.ColorFilter(0, 0, 0, 1, gold.r, gold.g, gold.b, 0)
    ];

    //caching and adding to cont
    var bounds = text_obj.getBounds();
    var w = bounds.width;
    var h = bounds.height;
    command_window.cont.addChild(text_obj);
    text_obj.cache(0, 0, w*2, h*2);

    ch_no += ch.length

    text = ": " + text;
    var length = 1 + text.length; // +1 for :

    var initial_text = text.slice(0, offset_width-ch_no);
    
    text_obj = new createjs.BitmapText(initial_text, cursed.ss);
    text_obj.x = ch_no * (cursed.constants.font_size+cursed.constants.font_width_offset);
    text_obj.y = cursed.constants.font_size * line_no;
    text_obj.letterSpacing = cursed.constants.font_spacing;

    //setting color
    text_obj.filters = [
        new createjs.ColorFilter(0, 0, 0, 1, white.r, white.g, white.b, 0)
    ];

    bounds = text_obj.getBounds();
    w = bounds.width;
    h = bounds.height;
    command_window.cont.addChild(text_obj);
    text_obj.cache(0, 0, w*2, h*2);

    line_no += 1;


    if(ch_no + length > offset_width){
        var left_over = text.slice(offset_width - ch_no, text.length);
        var split_text = left_over.match(new RegExp('.{1,' + offset_width + '}', "g"));

        for(var t of split_text){

            //creating and positioning
            var text_obj = new createjs.BitmapText(t, cursed.ss);
            text_obj.x = 0;
            text_obj.y = cursed.constants.font_size * line_no;
            text_obj.letterSpacing = cursed.constants.font_spacing;

            //setting color
            text_obj.filters = [
                new createjs.ColorFilter(0, 0, 0, 1, white.r, white.g, white.b, 0)
            ];

            //caching and adding to cont
            var bounds = text_obj.getBounds();
            var w = bounds.width;
            var h = bounds.height;
            command_window.cont.addChild(text_obj);
            text_obj.cache(0, 0, w*2, h*2);

            line_no += 1;
        }
    }

    command_window.cont.updateCache();
    
    return line_no;
}

command_window.handle = function(e){

    if(command_window.mode === command_window.command_modes.default){
        if(e.key === "b" && cursed.state.role === "gm"){
            command_window.mode = command_window.command_modes.build;
            command_window.dirty = true;
            command_window.draw();
        }
        else if(e.key ==="F" && cursed.state.role === "gm"){
            command_window.mode = command_window.command_modes.fow;
            command_window.dirty = true;
            command_window.draw();
        }
    }
    else if(command_window.mode === command_window.command_modes.build){
        if(e.key === "Escape"){
            command_window.mode = command_window.command_modes.default;
            command_window.dirty = true;
            command_window.draw();
            
        }

        var keybindings = [
            { key: "w", type: "Wall" },
            { key: "t", type: "Table" },
            { key: "c", type: "Chair" },
            { key: "d", type: "Door" },
            { key: ">", type: "Up Stair" },
            { key: "<", type: "Down Stair" },
            { key: "%", type: "Lantern" },
            { key: "r", type: "Road" },
            { key: "G", type: "Gate" },
            { key: "~", type: "Water" },
            { key: "t", type: "Tree" },
            { key: "o", type: "Bush" },
            { key: ".", type: "Grass" },
            { key: "^", type: "Hill" },
            { key: "b", type: "Bed" },
            { key: "&", type: "Statue" },
            { key: "B", type: "Blood" },
            { key: "f", type: "Fire" },
            { key: "s", type: "Snow" },
            { key: "O", type: "Boulder" }
        ];

        for(var binding of keybindings){
            if(e.key === binding.key){
                if(command_window.box){
                    //TODO: implement build menu bulk add
                }
                else{
                    var feature = cursed.features.get(binding.type);
                    var new_feature =  {
                        x: cursed.viewport.cursor_x,
                        y: cursed.viewport.cursor_y,
                        type: feature.name,
                        notes: ""
                    };

                    cursed.client.request("/map/add", new_feature, ()=>{});
                }
            }
        }

        if(e.key === "x"){
            if(command_window.box){
                //TODO: implement build menu bulk rm
            }
            else{
                cursed.client.request("/map/rm", {
                    x: cursed.viewport.cursor_x,
                    y: cursed.viewport.cursor_y,
                    
                }, ()=>{});
            }
        }
    }
}

command_window.handle_combo = function(buf){

}

command_window.handle_help = function(buf){

}

command_window.draw_pc_default_screen = function(){
    var line = command_window.draw_title(0, "Commands:");
    line = command_window.draw_key(line, "c", "Chat");
    line = command_window.draw_key(line, "u", "Users");
}

command_window.draw_gm_default_screen = function(){
    var line = command_window.draw_title(0, "Commands:");
    line = command_window.draw_key(line, "b", "Build");
    line = command_window.draw_key(line, "c", "Chat");
    line = command_window.draw_key(line, "n", "Narrative");
    line = command_window.draw_key(line, "f", "Toggle Fog of War for GM");
    line = command_window.draw_key(line, "F", "Edit Fog of War");
    line = command_window.draw_key(line, "u", "Units");
    line = command_window.draw_key(line, "m", "Maps");
    line = command_window.draw_key(line, "u", "Users");
}

command_window.draw_build_screen = function(){
    var line;
    if(command_window.box){
        line = command_window.draw_title(0, "Build (Box Mode):");
    }
    else{
        line = command_window.draw_title(0, "Build:");
    }

    line = command_window.draw_key(line, "w", "Wall");
    line = command_window.draw_key(line, "t", "Table");
    line = command_window.draw_key(line, "c", "Chair");
    line = command_window.draw_key(line, "d", "Door");
    line = command_window.draw_key(line, ">", "Up Stair");
    line = command_window.draw_key(line, "<", "Down Stair");
    line = command_window.draw_key(line, "%", "Lantern");
    line = command_window.draw_key(line, "r", "Road");
    line = command_window.draw_key(line, "#", "Chest");
    line = command_window.draw_key(line, "G", "Gate");
    line = command_window.draw_key(line, "~", "Water");
    line = command_window.draw_key(line, "t", "Tree");
    line = command_window.draw_key(line, "o", "Bush");
    line = command_window.draw_key(line, ".", "Grass");
    line = command_window.draw_key(line, "^", "Hill");
    line = command_window.draw_key(line, "b", "Bed");
    line = command_window.draw_key(line, "&", "Statue");
    line = command_window.draw_key(line, "B", "Blood");
    line = command_window.draw_key(line, "f", "Fire");
    line = command_window.draw_key(line, "s", "Snow");
    line = command_window.draw_key(line, "O", "Boulder");

    line = command_window.draw_key(line+1, "x", "Remove Object");
    line = command_window.draw_key(line, "space", "Select box corner");

    if(command_window.box){
        line = command_window.draw_key(line+2, "esc", "Select box Cancel Box Mode");
    }
    else{
        line = command_window.draw_key(line+2, "esc", "Back");
    }

}

command_window.draw_fow_screen = function(){

}

command_window.draw_units_screen = function(){

}

command_window.draw_unit_move_screen = function(){

}

command_window.draw_box_select_screen = function(){

}

