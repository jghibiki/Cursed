"use strict";

var status_line = {};

status_line.init = function(){

    status_line.y = cursed.constants.height - (3 * cursed.constants.font_size);
    status_line.x = Math.ceil(cursed.constants.width/2); 

    status_line.width = Math.ceil(cursed.constants.width/2);
    status_line.height = 3 * cursed.constants.font_size;

    status_line.rect_offset = Math.floor(cursed.constants.font_size/2)

};
status_line.draw = function(){
    
    /* Top Box */
    (function(){
        var box = new createjs.Shape();
        box.graphics.append(createjs.Graphics.beginCmd);

        box.graphics.append(new createjs.Graphics.Rect(
            status_line.x + status_line.rect_offset, 
            status_line.y+status_line.rect_offset, 
            status_line.width - 2*status_line.rect_offset, 
            Math.floor(cursed.constants.font_size/6)));
        
        box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

        cursed.stage.addChild(box);
    })();

    /* Bottom Box */
    (function(){
        var box = new createjs.Shape();
        box.graphics.append(createjs.Graphics.beginCmd);

        box.graphics.append(
            new createjs.Graphics.Rect(
                status_line.x + status_line.rect_offset, 
                (status_line.y + (status_line.height-cursed.constants.font_size)) + status_line.rect_offset, 
                status_line.width - 2*status_line.rect_offset, 
                Math.floor(cursed.constants.font_size/6)));
        
        box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

        cursed.stage.addChild(box);
    })();

    /* Left Box */
    (function(){
        var box = new createjs.Shape();
        box.graphics.append(createjs.Graphics.beginCmd);

        box.graphics.append(new createjs.Graphics.Rect(
            status_line.x + status_line.rect_offset, 
            status_line.y + status_line.rect_offset, 
            Math.floor((cursed.constants.font_size + cursed.constants.font_width_offset)/6), 
            status_line.height - 2*status_line.rect_offset));
        
        box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

        cursed.stage.addChild(box);
    })();

    /* Right Box */
    (function(){
        var box = new createjs.Shape();
        box.graphics.append(createjs.Graphics.beginCmd);

        box.graphics.append(
            new createjs.Graphics.Rect(
                status_line.x + status_line.width - status_line.rect_offset -1, //TODO: figure out odd 1 px offset
                status_line.y + status_line.rect_offset, 
                Math.floor((cursed.constants.font_size + cursed.constants.font_width_offset)/6), 
                status_line.height - status_line.rect_offset*2 ));
        
        box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

        cursed.stage.addChild(box);
    })();

    cursed.stage.update();
}
