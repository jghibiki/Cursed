"use strict";

var colon_line = {};

colon_line.init = function(){

    colon_line.y = cursed.constants.height - (3 * cursed.constants.font_size);
    colon_line.x = 0; 

    colon_line.width = Math.ceil(cursed.constants.width/2);
    colon_line.height = (3 * cursed.constants.font_size);

    colon_line.rect_offset = Math.floor(cursed.constants.font_size/2);

};
colon_line.draw = function(){
    
    /* Top Box */
    (function(){
        var box = new createjs.Shape();
        box.graphics.append(createjs.Graphics.beginCmd);

        box.graphics.append(new createjs.Graphics.Rect(
            colon_line.x + colon_line.rect_offset, 
            colon_line.y+colon_line.rect_offset, 
            colon_line.width - 2*colon_line.rect_offset, 
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
                colon_line.x + colon_line.rect_offset, 
                (colon_line.y + (colon_line.height-cursed.constants.font_size)) + colon_line.rect_offset, 
                colon_line.width - 2*colon_line.rect_offset, 
                Math.floor(cursed.constants.font_size/6)));
        
        box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

        cursed.stage.addChild(box);
    })();

    /* Left Box */
    (function(){
        var box = new createjs.Shape();
        box.graphics.append(createjs.Graphics.beginCmd);

        box.graphics.append(new createjs.Graphics.Rect(
            colon_line.x + colon_line.rect_offset, 
            colon_line.y + colon_line.rect_offset, 
            Math.floor((cursed.constants.font_size + cursed.constants.font_width_offset)/6), 
            colon_line.height - 2*colon_line.rect_offset));
        
        box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

        cursed.stage.addChild(box);
    })();

    /* Right Box */
    (function(){
        var box = new createjs.Shape();
        box.graphics.append(createjs.Graphics.beginCmd);

        box.graphics.append(
            new createjs.Graphics.Rect(
                (colon_line.width - (cursed.constants.font_size + cursed.constants.font_width_offset)), 
                colon_line.y + colon_line.rect_offset, 
                Math.floor((cursed.constants.font_size + cursed.constants.font_width_offset)/6), 
                colon_line.height - colon_line.rect_offset*2 ));
        
        box.graphics.append(new createjs.Graphics.Fill(cursed.colors.get("Gold").value));

        cursed.stage.addChild(box);
    })();


    colon_line.text = new createjs.BitmapText("asdfa", cursed.ss);
    colon_line.text.letterSpacing = cursed.constants.font_spacing;
    colon_line.text.x = colon_line.x + 15; // TODO: figure out better colon_line placement
    colon_line.text.y = colon_line.y + 12;

    var color_obj = cursed.colors.get("Gold");
    colon_line.text.filters = [
            new createjs.ColorFilter(0, 0, 0, 1, color_obj.r, color_obj.g, color_obj.b, 0)
    ];
    colon_line.text.cache(0, 0, colon_line.width, cursed.constants.font_size*2);
    cursed.stage.addChild(colon_line.text);

    cursed.stage.update();
}

colon_line.set_buff = function(buff){

    colon_line.text.text = buff;
    colon_line.text.cache(0, 0, colon_line.width, colon_line.height);
    cursed.viewer.dirty = true;
    
}

colon_line.clear_buff = function(){ 
    colon_line.text.text = "";
    colon_line.text.cache(0, 0, colon_line.width, colon_line.height);
    cursed.viewer.dirty = true;
}
