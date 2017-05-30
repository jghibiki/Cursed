"use strict";

var text_box = {
    dirty: true
};

text_box.init = function(){

    text_box.y = 0;
    text_box.x = 0; 

    text_box.width = Math.ceil(cursed.constants.width/3) - 1;
    var height = cursed.constants.height - (3 * cursed.constants.font_size);
    var correction = height % cursed.constants.font_size;
    text_box.height = height - correction; 

    text_box.page = 0;
    text_box.first_draw = true;
    text_box.text_container = new createjs.Container();
    text_box.text_container.x = cursed.constants.font_size;
    text_box.text_container.y = cursed.constants.font_size;
	//text_box.text_container.cache(0, 0, text_box.width, text_box.height);

    //initial text
    text_box.default_lines = [
        [
            {
                "text": "Text Box:" ,
                "color": "Gold"
            }
        ],
        [
            {
                "text": "ctrl + j",
                "color": "Gold"
            },
            {
                "text": " - scroll down",
                "color": null
            }
        ],
        [
            {
                "text": "ctrl + k" ,
                "color": "Gold"
            },
            {
                "text": " - scroll up",
                "color": null
            }
        ],
        [
            {
                "text": ":clear",
                "color": "Gold"
            },
            {
                "text": " - clear text box.",
                "color": null
            }

        ],
        [
            {
                "text": ":read",
                "color": "Gold"
            },
            {
                "text": " - read text in window. GM only.",
                "color": null
            }
        ],
        [
            {
                "text":  "Narrative (GM Only):",
                "color": "Gold"
            }
        ],
        [
            {
                "text": ":n list",
                "color": "Gold"
            },
            {
                "text": " - list chapters.",
                "color": null
            }
        ],
        [
            {
                "text": ":n view <chapter number>",
                "color": "Gold"
            },
            {
                "text": " - view chapter.",
                "color": null
            }
        ],
        [
            {
                "text": ":n edit <chapter number>",
                "color": "Gold"
            },
            {
                "text": " - edit chapter.",
                "color": null
            }
        ],
        [
            {
                "text": "Chat:",
                "color": "Gold"
            }
        ],
        [
            {
                "text": ":chat <message>",
                "color": "Gold"
            },
            {
                "text": " - send a message to all players",
                "color": null
            }
        ],
        [
            {
                "text": ":whisper <username> <message>",
                "color": "Gold"
            },
            {
                "text": " - send a message to a specific player",
                "color": null
            }
        ]
    ];

    text_box.text = text_box.default_lines;
    text_box.rendered_text = null;
    text_box.handling_page = false;
    cursed.modules.interactive.push(text_box);
};
text_box.draw = function(){
    if(text_box.dirty){
    
        if(text_box.first_draw){
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

            cursed.stage.addChild(text_box.text_container);


            text_box.first_draw = false;
        }
        
        /* draw text */
        text_box.text_container.removeAllChildren();

        if(text_box.rendered_text === null){
            text_box.render_text();
        }

        var max_entry = 50; //TODO make rows to render scale
        if(max_entry > text_box.text.length){
            max_entry = text_box.text.length;
            text_box.page = text_box.page - 1 >= 0? text_box.page-1: text_box.page;
        }

        var page_counter = 0;
        var line_no = 0;
        for(var i=0; i<text_box.rendered_text.length; i++){
            var line = text_box.rendered_text[i];
            if(page_counter < text_box.page || page_counter > max_entry+text_box.page){
                line_no = 0;
                page_counter += 1
                continue;
            } 
            else{
                for(var line_part of line){

                    line_part.y = (line_no * cursed.constants.font_size);
                    text_box.text_container.addChild(line_part);

                }
                page_counter += 1;
                line_no += 1;
            }
        }

        text_box.handling_page = false;

		//text_box.text_container.updateCache();
        text_box.dirty = false;
        cursed.viewer.dirty = true;
    }
}

text_box.set = function(text){
    text_box.rendered_text = null;
    text_box.text = text;
    text_box.dirty = true;
    text_box.page = 0;
    text_box.draw();
};

text_box.handle = function(e){

    if(! text_box.handling_page){
        if(e.key === "PageDown"){
            text_box.handling_page = true;
            text_box.page += 10;
            text_box.dirty = true;
            text_box.draw();
        }

        if(e.key === "PageUp"){
            if(text_box.page - 10 >= 0){
                text_box.handling_page = true;
                text_box.page -= 10;
                text_box.dirty = true;
                text_box.draw();
            }
            else if(text_box.page - 1 >= 0){
                text_box.handling_page = true;
                text_box.page -= 1;
                text_box.dirty = true;
                text_box.draw();
            }
        }
    }

}

text_box.handle_help = function(buff){

}

text_box.handle_combo = function(buff){
    
    if(buff == "clear"){
        text_box.set(text_box.default_lines);
    }
}

text_box.render_text = function(){
    console.log("rendering text")
    var line_no = 0;
    var line_width = text_box.width  - (cursed.constants.font_size * 3)

    var rendered_lines = [];
    for(var line of text_box.text){
        var ch = 0; //number of characters in line so far

        var broken = false;
        
        //TODO fix issue with not paging wrapped lines
        //TODO fix issue with missing letter when wrapping line

        var current_line = [];
        part_loop: for(var part of line){
            //if(page_counter < text_box.page || page_counter > max_entry+text_box.page){
            //    line_no = 0;
            //    page_counter += 1
            //    broken = true;
            //    break;
            //}

            var color_obj = null
            if(part.hasOwnProperty("color") && part.color !== null){
                color_obj = cursed.colors.get(part.color);
            }
            else{
                color_obj = cursed.colors.get("White");
            }


            if(part.text.length > 0){
                var overflow_buff = part.text.replace(/[\n\r]+/g, '');
            }
            else{ var overflow_buff = ""; }
            var buff = overflow_buff[0];
            overflow_buff = overflow_buff.slice(1, overflow_buff.length);


            buff_loop: while(buff !== undefined && (buff.length > 0 || overflow_buff.length > 0)){
                var text = new createjs.BitmapText(buff, cursed.ss);
                text.letterSpacing = cursed.constants.font_spacing;

                while(text.getBounds().width + ch < line_width && overflow_buff.length > 0){
                    var tmp = overflow_buff[0];
                    overflow_buff = overflow_buff.slice(1, overflow_buff.length);
                    buff = buff + tmp;
                    text = new createjs.BitmapText(buff, cursed.ss);
                    text.letterSpacing = cursed.constants.font_spacing;
                }


                if(buff.length > 1){

                    text.x = ch;

                    text.filters = [
                        new createjs.ColorFilter(0, 0, 0, 1, color_obj.r, color_obj.g, color_obj.b, 0)
                    ];

                    var bounds = text.getBounds();
                    var w = bounds.width;
                    var h = bounds.height;
                    //text_box.text_container.addChild(text);
                    current_line.push(text);

                    ch += w;

                    if (overflow_buff.length > 0){
                        buff = overflow_buff[0];
                        overflow_buff = overflow_buff.slice(1, overflow_buff.length);
                    }
                    else{ 
                        buff = "";
                        continue; 
                    }
                }
                if(buff.length == 1 && overflow_buff.length == 0){
                    ch = 0;

                    text.x = ch;

                    text.filters = [
                        new createjs.ColorFilter(0, 0, 0, 1, color_obj.r, color_obj.g, color_obj.b, 0)
                    ];

                    var bounds = text.getBounds();
                    var w = bounds.width;
                    var h = bounds.height;
                    //text_box.text_container.addChild(text);
                    current_line.push(text);
                    rendered_lines.push(current_line);
                    current_line = [];

                    ch += w;

                    var buff = overflow_buff[0];
                    overflow_buff = overflow_buff.slice(1, overflow_buff.length);

                }
                else{
                    ch = 0;
                    //var buff = overflow_buff[0];
                    //overflow_buff = overflow_buff.slice(1, overflow_buff.length);

                    rendered_lines.push(current_line);
                    current_line = [];
                }

            }
        }


        ch = 0;
        rendered_lines.push(current_line);
        current_line = [];
    }

    // update cache for all lines
    for(var i=0; i<rendered_lines.length; i++){
        var line = rendered_lines[i];
        for(var line_part of line){

            line_part.letterSpacing = cursed.constants.font_spacing;
            line_part.lineHeight = cursed.constants.font_size*2;

            var bounds = line_part.getBounds();
            var w = bounds.width;
            var h = bounds.height;
            line_part.cache(0, 0, w*2, h*2);
        }
    }

    text_box.rendered_text = rendered_lines;
}
