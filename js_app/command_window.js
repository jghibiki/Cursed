"use strict";

var command_window = {};

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

};
command_window.draw = function(){
    
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


    cursed.stage.update();
}
