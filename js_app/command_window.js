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
        box_select: 5,
        initiative: 6,
        initiative_unit_select: 7
    },
    
    //box select vars
    box: false,
    box_referer: -1,
    box_xy_1: null,
    box_xy_2: null,
    box_returning: false,

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
        else if(command_window.mode === command_window.command_modes.build){
            command_window.draw_build_screen();
        }
        else if(command_window.mode === command_window.command_modes.fow){
            command_window.draw_fow_screen();
        }
        else if(command_window.mode === command_window.command_modes.box_select){
            command_window.draw_box_select_screen();
        }
        else if(command_window.mode === command_window.command_modes.units){
            command_window.draw_units_screen();
        }
        else if(command_window.mode === command_window.command_modes.unit_move){
            command_window.draw_unit_move_screen();
        }
        else if(command_window.mode === command_window.command_modes.initiative){
            command_window.draw_initiative_screen();
        }
        else if(command_window.mode === command_window.command_modes.initiative_unit_select){
            command_window.draw_initiative_unit_select_screen();
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

command_window.draw_key = function(line_no, ch, text, color){
    var offset_width = Math.floor(
        command_window.width/(
            cursed.constants.font_size + cursed.constants.font_width_offset)
    )-5;

    
    var split_text = text.match(new RegExp('.{1,' + offset_width + '}', "g"));
    var white = cursed.colors.get("White");

    var ch_no = 0;
    
    // Adding character text
    //creating and positioning
    var text_obj = new createjs.BitmapText(ch, cursed.ss);
    text_obj.x = 0;
    text_obj.y = cursed.constants.font_size * line_no;
    text_obj.letterSpacing = cursed.constants.font_spacing;

    //setting color
    if(color === null || color == undefined){
        var gold = cursed.colors.get("Gold");
        text_obj.filters = [
            new createjs.ColorFilter(0, 0, 0, 1, gold.r, gold.g, gold.b, 0)
        ];
    }
    else{
        var color_obj = cursed.colors.get(color);
        text_obj.filters = [
            new createjs.ColorFilter(0, 0, 0, 1, color_obj.r, color_obj.g, color_obj.b, 0)
        ];
    }

    //caching and adding to cont
    var bounds = text_obj.getBounds();
    var w = bounds.width;
    var h = bounds.height;
    command_window.cont.addChild(text_obj);
    text_obj.cache(0, 0, w*2, h*2);

    ch_no += ch.length 

    text = " : " + text;
    var length =  2 + text.length; // +1 for :

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
        var left_over = text.slice(offset_width - ch_no -1, text.length);
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
        else if(e.key ==="u"){
            command_window.mode = command_window.command_modes.units;
            command_window.dirty = true;
            command_window.draw();
        }else if(e.key === "!"){
            command_window.mode = command_window.command_modes.initiative;
            command_window.dirty = true;
            command_window.draw();
            cursed.initiative.show();
        }
    }
    else if(command_window.mode === command_window.command_modes.build){
        if(e.key === "Escape"){
            if(command_window.box){
                command_window.box = false;
                command_window.dirty = true;
                command_window.draw();

                cursed.viewport.box_xy = null;
                cursed.viewport.dirty = true;
                cursed.viewport.draw();
            }
            else{
                command_window.mode = command_window.command_modes.default;
                command_window.dirty = true;
                command_window.draw();
            }
        }

        for(var feature of cursed.features.objects){
            if(e.key === feature.key){
                if(command_window.box){
                    var x_min = Math.min(command_window.box_xy_1[0], command_window.box_xy_2[0]) + viewport.v_x;
                    var x_max = Math.max(command_window.box_xy_1[0], command_window.box_xy_2[0]) + viewport.v_x + 1;

                    var y_min = Math.min(command_window.box_xy_1[1], command_window.box_xy_2[1]) + viewport.v_y;
                    var y_max = Math.max(command_window.box_xy_1[1], command_window.box_xy_2[1]) + viewport.v_y + 1;

                    var frames = [];

                    for(var i=y_min; i < y_max; i++){
                        for(var j=x_min; j < x_max; j++){
                            frames.push({
                                type: "command",
                                key: "add.map.feature",
                                details: {
                                    x: j,
                                    y: i,
                                    type: feature.name,
                                    notes: ""
                                }
                            });
                        }
                    }

                    cursed.client.sendBulk(frames, true);

                    command_window.box_xy_1 = null;
                    command_window.box_xy_2 = null;

                    command_window.box = false;
                    command_window.dirty = true;
                    command_window.draw();

                    cursed.viewport.box_xy = null;
                    cursed.viewport.dirty = true;
                    cursed.viewport.draw();

                }
                else{
                    var new_feature =  {
                        x: cursed.viewport.cursor_x + cursed.viewport.v_x,
                        y: cursed.viewport.cursor_y + cursed.viewport.v_y,
                        type: feature.name,
                        notes: ""
                    };
                    cursed.client.send({
                        type: "command",
                        key: "add.map.feature",
                        details: new_feature
                    }, true);
                }
            }
        }

        if(e.key === "x"){
            if(command_window.box){
                var x_min = Math.min(command_window.box_xy_1[0], command_window.box_xy_2[0]) + viewport.v_x;
                var x_max = Math.max(command_window.box_xy_1[0], command_window.box_xy_2[0]) + viewport.v_x + 1;

                var y_min = Math.min(command_window.box_xy_1[1], command_window.box_xy_2[1]) + viewport.v_y;
                var y_max = Math.max(command_window.box_xy_1[1], command_window.box_xy_2[1]) + viewport.v_y + 1;

                var frames = [];

                for(var i=y_min; i < y_max; i++){
                    for(var j=x_min; j < x_max; j++){
                        frames.push({
                            type: "command",
                            key: "remove.map.feature",
                            details: {
                                x: j,
                                y: i
                            }
                        });
                    }
                }

                cursed.client.sendBulk(frames, true);

                command_window.box_xy_1 = null;
                command_window.box_xy_2 = null;

                command_window.box = false;
                command_window.dirty = true;
                command_window.draw();

                cursed.viewport.box_xy = null;
                cursed.viewport.dirty = true;
                cursed.viewport.draw();
            }
            else{
                cursed.client.send({
                    type: "command",
                    key: "remove.map.feature",
                    details: {
                        x: cursed.viewport.cursor_x + cursed.viewport.v_x,
                        y: cursed.viewport.cursor_y + cursed.viewport.v_y,
                    }
                }, true);
            }
        }
        else if(e.key === " "){
            command_window.box_referer = command_window.command_modes.build;
            command_window.box_xy_1 = [ 
                cursed.viewport.cursor_x,
                cursed.viewport.cursor_y,
            ];
            cursed.viewport.box_xy = command_window.box_xy_1;
            cursed.viewport.dirty = true;
            cursed.viewport.draw();

            command_window.mode = command_window.command_modes.box_select;
            command_window.box = true;
            command_window.dirty = true;
            command_window.draw();
        }
    }
    else if(command_window.mode === command_window.command_modes.fow){
        if(e.key === "Escape"){
            if(command_window.box){
                command_window.box = false;
                command_window.dirty = true;
                command_window.draw();

                cursed.viewport.box_xy = null;
                cursed.viewport.dirty = true;
                cursed.viewport.draw();
            }
            else{
                command_window.mode = command_window.command_modes.default;
                command_window.dirty = true;
                command_window.draw();
            }
        }
        else if(e.key === " "){
            command_window.box_referer = command_window.command_modes.fow;
            command_window.box_xy_1 = [ 
                cursed.viewport.cursor_x,
                cursed.viewport.cursor_y,
            ];
            cursed.viewport.box_xy = command_window.box_xy_1;
            cursed.viewport.dirty = true;
            cursed.viewport.draw();

            command_window.mode = command_window.command_modes.box_select;
            command_window.box = true;
            command_window.dirty = true;
            command_window.draw();
        }
        else if(e.key === "a"){
            if(command_window.box){
                var x_min = Math.min(command_window.box_xy_1[0], command_window.box_xy_2[0]);
                var x_max = Math.max(command_window.box_xy_1[0], command_window.box_xy_2[0]) + 1;

                var y_min = Math.min(command_window.box_xy_1[1], command_window.box_xy_2[1]);
                var y_max = Math.max(command_window.box_xy_1[1], command_window.box_xy_2[1]) + 1;

                var frames = [];

                for(var i=y_min; i < y_max; i++){
                    for(var j=x_min; j < x_max; j++){
                        frames.push({
                            type: "command",
                            key: "add.map.fow",
                            details: {
                                x: j,
                                y: i
                            }
                        });
                    }
                }

                cursed.client.sendBulk(frames, true);

                command_window.box_xy_1 = null;
                command_window.box_xy_2 = null;

                command_window.box = false;
                command_window.dirty = true;
                command_window.draw();

                cursed.viewport.box_xy = null;
                cursed.viewport.dirty = true;
                cursed.viewport.draw();
            }
            else{
                cursed.client.send({
                    type: "command",
                    key: "add.map.fow",
                    details: {
                        x: cursed.viewport.cursor_x,
                        y: cursed.viewport.cursor_y,
                    }
                }, true);
            }
        }
        else if(e.key === "r"){
            if(command_window.box){
                var x_min = Math.min(command_window.box_xy_1[0], command_window.box_xy_2[0]);
                var x_max = Math.max(command_window.box_xy_1[0], command_window.box_xy_2[0]) + 1;

                var y_min = Math.min(command_window.box_xy_1[1], command_window.box_xy_2[1]);
                var y_max = Math.max(command_window.box_xy_1[1], command_window.box_xy_2[1]) + 1;

                var frames = [];

                for(var i=y_min; i < y_max; i++){
                    for(var j=x_min; j < x_max; j++){
                        frames.push({
                            type: "command",
                            key: "remove.map.fow",
                            details: {
                                x: j,
                                y: i
                            }
                        });
                    }
                }

                cursed.client.sendBulk(frames, true);

                command_window.box_xy_1 = null;
                command_window.box_xy_2 = null;

                command_window.box = false;
                command_window.dirty = true;
                command_window.draw();

                cursed.viewport.box_xy = null;
                cursed.viewport.dirty = true;
                cursed.viewport.draw();
            }
            else{
                cursed.client.send({
                    type: "command",
                    key: "remove.map.fow",
                    details: {
                        x: cursed.viewport.cursor_x,
                        y: cursed.viewport.cursor_y,
                    }
                }, true);
            }
        }

        if(!command_window.box){
            if(e.key === "A"){
                // TODO: implement fow fill
                //cursed.client.request("/fow/fill", null, ()=>{});
            }
            else if(e.key === "R"){
                // TODO: implement fow clear
                // cursed.client.request("/fow/clear", null, ()=>{});
            }

        }
    }
    else if(command_window.mode === command_window.command_modes.box_select){
        if(e.key === "Escape"){
            command_window.box_xy_1 = null;
            cursed.viewport.box_xy = command_window.box_xy_1;
            cursed.viewport.dirty = true;
            cursed.viewport.draw();

            command_window.mode = command_window.box_referer;
            command_window.box_referer = -1;
            command_window.dirty = true;
            command_window.box = false;
            command_window.draw();
        }
        else if(e.key === " "){
            command_window.box_xy_2 = [ 
                cursed.viewport.cursor_x,
                cursed.viewport.cursor_y,
            ];
            cursed.viewport.dirty = true;
            cursed.viewport.draw();


            command_window.mode = command_window.box_referer;
            command_window.box_referer = -1;
            command_window.dirty = true;
            command_window.box = true;
            command_window.draw();
        }
    }
    else if(command_window.mode === command_window.command_modes.units){
        if(e.key === "Escape"){
            command_window.mode = command_window.command_modes.default;
            command_window.dirty = true;
            command_window.draw();
            
        }
        else if (e.key === "m"){
            var current_unit = cursed.viewport.getCurrentUnit();
            if(current_unit !== null &&  //unit is valid and 
                (current_unit.controller === cursed.state.username || //user is controller
                 cursed.state.role === "gm") ){ // or the gm
                command_window.mode = command_window.command_modes.unit_move;
                command_window.dirty = true;
                command_window.draw();
            }
        }
        else if(e.key === "a"){
            //$("#text").val(data.text);
            var el = $("#unit_menu");
            el.prop("title", "Add Unit");
            el.dialog({
                resizable: true,
                height: "auto",
                width: "20%",
                modal: true,
                open: function(){

                    // pause keypress handling
                    cursed.viewer.editor_open = true;               

                    //blur text box - prevents issue with keybind char getting caught
                    $("#unit_name").val("");
                    $("#unit_name").blur();

                    $("#current_health").val("");
                    $("#max_health").val("");
                    $("#controller").val("");
                    $("#unit_type").val("");
                },
                close: function(){
                    // allow client to handle keypresses again
                    cursed.viewer.editor_open = false;               
                },
                buttons: {
                    "Add": function(){

                        var unit_name = $("#unit_name").val();
                        if(unit_name === null 
                            || unit_name === undefined
                            || unit_name === ""){
                            $("#validation").text("Unit Name must not be empty");
                            return;
                        }

                        var current_health = $("#current_health").val();
                        var valid_int = false;
                        try{
                            current_health = parseInt(current_health);
                            valid_int = true;
                        }
                        catch(e){
                            valid_int = false;
                        }
                        if(current_health === null 
                            || current_health === undefined 
                            || current_health === ""
                            || !valid_int){
                            $("#validation").text("Current Health must not be empty and be a valid integer.");
                            return;
                        }

                        var max_health = $("#max_health").val();
                        var valid_int = false;
                        try{
                            max_health = parseInt(max_health);
                            valid_int = true;
                        }
                        catch(e){
                            valid_int = false;
                        }
                        if(max_health === null 
                            || max_health === undefined 
                            || max_health === ""
                            || !valid_int){
                            $("#validation").text("Max Health must not be empty and be a valid integer.");
                            return;
                        }

                        var controller = $("#controller").val();
                        if(controller === null 
                            || controller === undefined
                            || controller === ""){
                            $("#validation").text("Controller Name must not be empty");
                            return;
                        }

                        var type = $("#unit_type").val();
                        if(type === null 
                            || type === undefined
                            || type === ""){
                            $("#validation").text("A Unit Type must be selected.");
                            return;
                        }

                        var details = {
                            x: cursed.viewport.cursor_x,
                            y: cursed.viewport.cursor_y,
                            name: unit_name,
                            current_health: current_health,
                            max_health: max_health,
                            controller: controller,
                            type: type,
                            id: Math.random().toString(36).substring(7)
                        }

                        cursed.client.send({
                            type: "command",
                            key: "add.map.unit",
                            details: details
                        }, true);

                        cursed.viewer.editor_open = false;               
                        $(this).dialog("close");
                    },
                    "Cancel": function(){
                        cursed.viewer.editor_open = false;               
                        $(this).dialog("close");
                    }
                }
            });
        }
        else if(e.key === "e"){
            var el = $("#unit_menu");
            el.prop("title", "Edit Unit");

            var unit = cursed.viewport.getCurrentUnit();

            $("#unit_name").val(unit.name);
            $("#current_health").val(unit.current_health);
            $("#max_health").val(unit.max_health);
            $("#controller").val(unit.controller);
            $("#unit_type").val(unit.type);

            el.dialog({
                resizable: true,
                height: "auto",
                width: "20%",
                modal: true,
                open: function(){

                    // pause keypress handling
                    cursed.viewer.editor_open = true;               

                    //blur text box - prevents issue with keybind char getting caught
                    $("#unit_name").blur();
                },
                close: function(){
                    // allow client to handle keypresses again
                    cursed.viewer.editor_open = false;               
                },
                buttons: {
                    "Save": function(){

                        var unit_name = $("#unit_name").val();
                        if(unit_name === null 
                            || unit_name === undefined
                            || unit_name === ""){
                            $("#validation").text("Unit Name must not be empty");
                            return;
                        }

                        var current_health = $("#current_health").val();
                        var valid_int = false;
                        try{
                            current_health = parseInt(current_health);
                            valid_int = true;
                        }
                        catch(e){
                            valid_int = false;
                        }
                        if(current_health === null 
                            || current_health === undefined 
                            || current_health === ""
                            || !valid_int){
                            $("#validation").text("Current Health must not be empty and be a valid integer.");
                            return;
                        }

                        var max_health = $("#max_health").val();
                        var valid_int = false;
                        try{
                            max_health = parseInt(max_health);
                            valid_int = true;
                        }
                        catch(e){
                            valid_int = false;
                        }
                        if(max_health === null 
                            || max_health === undefined 
                            || max_health === ""
                            || !valid_int){
                            $("#validation").text("Max Health must not be empty and be a valid integer.");
                            return;
                        }

                        var controller = $("#controller").val();
                        if(controller === null 
                            || controller === undefined
                            || controller === ""){
                            $("#validation").text("Controller Name must not be empty");
                            return;
                        }

                        var type = $("#unit_type").val();
                        if(type === null 
                            || type === undefined
                            || type === ""){
                            $("#validation").text("A Unit Type must be selected.");
                            return;
                        }

                        var unit = cursed.viewport.getCurrentUnit();
                        unit.name = unit_name;
                        unit.current_health = current_health;
                        unit.max_health = max_health;
                        unit.controller = controller;
                        unit.type = type;

                        cursed.client.send({
                            type: "command",
                            key: "modify.map.unit",
                            details: unit
                        }, true);

                        cursed.viewer.editor_open = false;               
                        $(this).dialog("close");
                    },
                    "Cancel": function(){
                        cursed.viewer.editor_open = false;               
                        $(this).dialog("close");
                    }
                }
            });
        }
        if(e.key === "r"){
            //TODO: add dialog to confirm?
            var unit = cursed.viewport.getCurrentUnit();

            cursed.client.send({
                type: "command",
                key: "remove.map.unit",
                details: {
                    id: unit.id
                }
            }, true);
        }
    }
    else if(command_window.mode === command_window.command_modes.unit_move){
        if(e.key === "Escape"){
            command_window.mode = command_window.command_modes.units;
            command_window.dirty = true;
            command_window.draw();
            
        }
        else if(
            (cursed.state.move_mode === "hjkl" && e.key === "j") ||
            (cursed.state.move_mode === "ijkl" && e.key === "k") ){
            var current_unit = cursed.viewport.getCurrentUnit();

            if(current_unit.y +1 <= cursed.viewport.height){
                var modified_unit = {
                    "x": current_unit["x"],
                    "y": current_unit["y"] + 1,
                    "max_health": current_unit["max_health"],
                    "current_health": current_unit["current_health"],
                    "controller": current_unit["controller"],
                    "type": current_unit["type"],
                    "id": current_unit["id"],
                    "name": current_unit["name"]
                }
                cursed.viewport.cursor_down();
                cursed.client.send({
                    type: "command",
                    key: "modify.map.unit",
                    details: modified_unit
                }, true);
            }
        }
        else if(
            (cursed.state.move_mode === "hjkl" && e.key === "k") ||
            (cursed.state.move_mode === "ijkl" && e.key === "i") ){
            var current_unit = cursed.viewport.getCurrentUnit();

            if(current_unit.y-1 >= 0){
                var modified_unit = {
                    "x": current_unit["x"],
                    "y": current_unit["y"] - 1,
                    "max_health": current_unit["max_health"],
                    "current_health": current_unit["current_health"],
                    "controller": current_unit["controller"],
                    "type": current_unit["type"],
                    "id": current_unit["id"],
                    "name": current_unit["name"]
                }
                cursed.viewport.cursor_up();
                cursed.client.send({
                    type: "command",
                    key: "modify.map.unit",
                    details: modified_unit
                }, true);
            }
        }
        else if(
            (cursed.state.move_mode === "hjkl" && e.key === "h") ||
            (cursed.state.move_mode === "ijkl" && e.key === "j") ){
            var current_unit = cursed.viewport.getCurrentUnit();

            if(current_unit.x-1 >= 0){
                var modified_unit = {
                    "x": current_unit["x"] - 1,
                    "y": current_unit["y"],
                    "max_health": current_unit["max_health"],
                    "current_health": current_unit["current_health"],
                    "controller": current_unit["controller"],
                    "type": current_unit["type"],
                    "id": current_unit["id"],
                    "name": current_unit["name"]
                }
                cursed.viewport.cursor_left();
                cursed.client.send({
                    type: "command",
                    key: "modify.map.unit",
                    details: modified_unit
                }, true);
            }
        }
        else if(
            (cursed.state.move_mode === "hjkl" && e.key === "l") ||
            (cursed.state.move_mode === "ijkl" && e.key === "l") ){
            var current_unit = cursed.viewport.getCurrentUnit();

            if(current_unit.x+1 <= cursed.viewport.width){
                var modified_unit = {
                    "x": current_unit["x"] + 1,
                    "y": current_unit["y"],
                    "max_health": current_unit["max_health"],
                    "current_health": current_unit["current_health"],
                    "controller": current_unit["controller"],
                    "type": current_unit["type"],
                    "id": current_unit["id"],
                    "name": current_unit["name"]
                }
                cursed.viewport.cursor_right();
                cursed.client.send({
                    type: "command",
                    key: "modify.map.unit",
                    details: modified_unit
                }, true);
            }
        }
    }
    else if(command_window.mode === command_window.command_modes.initiative){
        if(e.key === "Escape"){
            command_window.mode = command_window.command_modes.default;
            command_window.dirty = true;
            command_window.draw();
        }
        else if(e.key === "s" && !cursed.initiative.encounter_started){
            cursed.initiative.show();
            command_window.mode = command_window.command_modes.initiative_unit_select;
            command_window.dirty = true;
            command_window.draw();
        }
        else if(e.key === "!"){
            cursed.initiative.show();
        }
        else if(e.key === "p"){
            cursed.initiative.selectPrevious();
        }
        else if(e.key === "n"){
            cursed.initiative.selectNext();
        }
        else if(e.key === "b" && !cursed.initiative.encounter_started){
            cursed.initiative.beginEncounter();
            command_window.mode = command_window.command_modes.initiative;
            command_window.dirty = true;
            command_window.draw();
        }
        else if(e.key === "e" && cursed.initiative.encounter_started){
            cursed.initiative.endEncounter();
            command_window.mode = command_window.command_modes.initiative;
            command_window.dirty = true;
            command_window.draw();
        }
        else if(e.key === "<" && !cursed.initiative.encounter_started){
            cursed.initiative.decreaseModifier();
        }
        else if(e.key === ">" && !cursed.initiative.encounter_started){
            cursed.initiative.increaseModifier();
        }
    }
    else if(command_window.mode === command_window.command_modes.initiative_unit_select){
        if(e.key === "Escape"){
            command_window.mode = command_window.command_modes.initiative;
            command_window.dirty = true;
            command_window.draw();
            
        }
        else if(e.key === "a"){
            cursed.initiative.addUnit();
        }
        else if(e.key === "r"){
            cursed.initiative.removeUnit();
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
    line = command_window.draw_key(line, "!", "Initiative");
}

command_window.draw_build_screen = function(){
    var line;
    if(command_window.box){
        line = command_window.draw_title(0, "Build (Box Mode):");
    }
    else{
        line = command_window.draw_title(0, "Build:");
    }

    for(var feature of cursed.features.objects.sort((a, b)=>{
        return a.name.localeCompare(b.name);
    })){
        line = command_window.draw_key(line, feature.key, feature.name);
    }

    line = command_window.draw_key(line+1, "x", "Remove Object");
    line = command_window.draw_key(line, "space", "Select box corner");

    if(command_window.box){
        line = command_window.draw_key(line+2, "esc", "Cancel Box Mode");
    }
    else{
        line = command_window.draw_key(line+2, "esc", "Back");
    }

}

command_window.draw_fow_screen = function(){
    var line;
    if(command_window.box){
        line = command_window.draw_title(0, "Fog of War (Box Mode):");
    }
    else{
        line = command_window.draw_title(0, "Fog of War:");
    }

    if(!command_window.box){
        line = command_window.draw_key(line, "f", "Toggle FoF for GM");
    }

    line = command_window.draw_key(line, "a", "Add FoW");
    line = command_window.draw_key(line, "r", "Remove FoW");

    if(!command_window.box){
        line = command_window.draw_key(line, "A", "Fill map with FoW");
        line = command_window.draw_key(line, "R", "Clear FoW");
    }

    line = command_window.draw_key(line+1, "space", "Select box corner");

    if(command_window.box){
        line = command_window.draw_key(line+2, "esc", "Cancel Box Mode");
    }
    else{
        line = command_window.draw_key(line+2, "esc", "Back");
    }
}

command_window.draw_units_screen = function(){
    var line;

    var current_unit = cursed.viewport.getCurrentUnit();
    line = command_window.draw_title(0, "Units:");
    if(cursed.state.role === "gm"){
        line = command_window.draw_key(line, "a", "Add Unit");

        if(current_unit !== null){
            line = command_window.draw_key(line, "r", "Remove Unit");
            line = command_window.draw_key(line, "m", "Move Unit");
            line = command_window.draw_key(line, "e", "Edit Unit");
            line = command_window.draw_key(line, "+", "Increase Unit Health");
            line = command_window.draw_key(line, "-", "Decrease Unit Health");
        }
        else {
            line = command_window.draw_key(line, "r", "Remove Unit", "Dark Grey");
            line = command_window.draw_key(line, "m", "Move Unit", "Dark Grey");
            line = command_window.draw_key(line, "e", "Edit Unit", "Dark Grey");
            line = command_window.draw_key(line, "+", "Increase Unit Health", "Dark Grey");
            line = command_window.draw_key(line, "-", "Decrease Unit Health", "Dark Grey");
        }

    }
    else if(cursed.state.role === "pc"){
        if(current_unit !== null){
            line = command_window.draw_key(line, "m", "Move Unit");
        }
        else {
            line = command_window.draw_key(line, "m", "Move Unit", "Dark Grey");
        }
    }

    line = command_window.draw_key(line+2, "esc", "Back");
}

command_window.draw_unit_move_screen = function(){
    var line = command_window.draw_title(0, "Move Unit:");
    line = command_window.draw_key(line, "j", "Down");
    line = command_window.draw_key(line, "k", "Up");
    line = command_window.draw_key(line, "h", "Left");
    line = command_window.draw_key(line, "l", "Right");

    line = command_window.draw_key(line+2, "esc", "Back");
}

command_window.draw_box_select_screen = function(){
    var line = command_window.draw_title(0, "Box Select");
    line = command_window.draw_key(line, "space", "Select box corner");
    line = command_window.draw_key(line, "esc", "Cancel");
}

command_window.draw_initiative_screen = function(){
    var line = command_window.draw_title(0, "Initiative:");
    if(!cursed.initiative.encounter_started){
        line = command_window.draw_key(line, "s", "Select/Unselect Units");
    }
    line = command_window.draw_key(line, "!", "Show encounter units");

    if(!cursed.initiative.encounter_started){
        line = command_window.draw_key(line, "b", "Begin Encounter");
    }
    else if(cursed.initiative.encounter_started){
        line = command_window.draw_key(line, "e", "End Encounter");
    }


    line = command_window.draw_key(line+1, "n", "Next Unit");
    line = command_window.draw_key(line, "p", "Previous Unit");

    if(!cursed.initiative.encounter_started){
        line = command_window.draw_key(line+1, "<", "Decrease Unit Modifier");
        line = command_window.draw_key(line, ">", "Increase Unit Modifier");
    }

    line = command_window.draw_key(line+2, "esc", "Back");
}

command_window.draw_initiative_unit_select_screen = function(){
    var line = command_window.draw_title(0, "Initiative Unit Select:");
    line = command_window.draw_key(line, "a", "Select Unit");
    line = command_window.draw_key(line, "r", "Unselect Unit");

    line = command_window.draw_key(line+2, "esc", "Back");
}
