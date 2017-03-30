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
        var line_no = 0;
        var line_width = text_box.width  - (cursed.constants.font_size * 3)

        var paged_text = text_box.text.slice(text_box.page, text_box.text.length);
        for(var line of paged_text){
            var ch = 0; //number of characters in line so far
            
            for(var part of line){
                var color_obj = null
                if(part.hasOwnProperty("color") && part.color !== null){
                    color_obj = cursed.colors.get(part.color);
                }
                else{
                    color_obj = cursed.colors.get("White");
                }


                var buff = part.text;
                var overflow_buff = ""

                while(buff.length > 0 || overflow_buff > 0){

                
                    var text = new createjs.BitmapText(buff, cursed.ss);
                    text.letterSpacing = cursed.constants.font_spacing;

                    while(text.getBounds().width + ch >= line_width && buff.length > 1){
                        var tmp = buff.substring(0, buff.length-1);
                        overflow_buff = buff.substring(buff.length-1, buff.length) + overflow_buff;
                        buff = tmp;
                        text = new createjs.BitmapText(buff, cursed.ss);
                        text.letterSpacing = cursed.constants.font_spacing;
                    }

                    if(buff.length > 1){

                        text.x = ch;
                        text.y = (line_no * cursed.constants.font_size);
                        text.letterSpacing = cursed.constants.font_spacing;
                        text.lineHeight = cursed.constants.font_size*2;

                        text.filters = [
                            new createjs.ColorFilter(0, 0, 0, 1, color_obj.r, color_obj.g, color_obj.b, 0)
                        ];

                        var bounds = text.getBounds();
                        var w = bounds.width;
                        var h = bounds.height;
                        text.cache(0, 0, w*2, h*2);
                        text_box.text_container.addChild(text);

                        ch += w;

                        buff = overflow_buff;
                        overflow_buff = "";

                    }
                    else{
                        ch = 0;
                        line_no += 1;
                        buff = buff + overflow_buff;
                        overflow_buff = "";
                    }
                }

            }

            ch = 0;
            line_no += 1;
        }

		//text_box.text_container.updateCache();
        text_box.dirty = false;
        cursed.viewer.dirty = true;
    }
}

text_box.set = function(text){
    text_box.text = text;
    text_box.dirty = true;
    text_box.page = 0;
    text_box.draw();
};

text_box.handle = function(e){

    if(e.key === "PageDown"){
        text_box.page += 1;
        text_box.dirty = true;
        text_box.draw();
    }

    if(e.key === "PageUp"){
		if(text_box.page > 0){
			text_box.page -= 1;
			text_box.dirty = true;
			text_box.draw();
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
