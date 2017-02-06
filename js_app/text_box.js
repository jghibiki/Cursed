"use strict";

var text_box = {};

text_box.init = function(){

    text_box.y = 0;
    text_box.x = 0; 

    text_box.width = Math.ceil(cursed.constants.width/3) - 1;
    var height = cursed.constants.height - (3 * cursed.constants.font_size);
    var correction = height % cursed.constants.font_size;
    text_box.height = height - correction; 

};
text_box.draw = function(){
    
    /* Top Box */
    (function(){
        var box = new createjs.Shape();
        box.graphics.append(createjs.Graphics.beginCmd);

        box.graphics.append(new createjs.Graphics.Rect(0, 0, text_box.width, cursed.constants.font_size));
        
        box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

        cursed.stage.addChild(box);
    })();

    /* Bottom Box */
    (function(){
        var box = new createjs.Shape();
        box.graphics.append(createjs.Graphics.beginCmd);

        box.graphics.append(new createjs.Graphics.Rect(0, text_box.height-cursed.constants.font_size, text_box.width, cursed.constants.font_size));
        
        box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

        cursed.stage.addChild(box);
    })();

    /* Left Box */
    (function(){
        var box = new createjs.Shape();
        box.graphics.append(createjs.Graphics.beginCmd);

        box.graphics.append(new createjs.Graphics.Rect(0, 0, cursed.constants.font_size + cursed.constants.font_width_offset, text_box.height));
        
        box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

        cursed.stage.addChild(box);
    })();

    /* Right Box */
    (function(){
        var box = new createjs.Shape();
        box.graphics.append(createjs.Graphics.beginCmd);

        box.graphics.append(
            new createjs.Graphics.Rect(
                text_box.width - (cursed.constants.font_size + cursed.constants.font_width_offset), 
                0, 
                cursed.constants.font_size + cursed.constants.font_width_offset, 
                text_box.height));
        
        box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

        cursed.stage.addChild(box);
    })();

    cursed.stage.update();
}
