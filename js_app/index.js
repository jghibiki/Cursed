"use strict";

var stage;
var queue;
var cursed = {
    constants: {
        font_size: 14,
        font_width_offset: -5,
        NUMBERS: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        IGNORE: ["Alt", "Ctrl", "Shift"]
    },
    state: {
        username: "",
        password: "",
        fow: "on"
    },
    viewer: {
        handling: false,
        dirty : true,
        combo_buffer: "",
        motion_buffer_count: ""
    },
    modules: {
        live: [],
        interactive: []
    }
};

function load(){
    queue = new createjs.LoadQueue(false);
    queue.addEventListener("complete", init);
    queue.loadManifest([
        {id: "jquery", src:"./third_party/jquery-3.1.1.min.js"},
        {id: "features", src: "./features.js"},
        {id: "colors", src: "./colors.js"},
        {id: "grid", src: "./grid.js"},
        {id: "command_window", src: "./command_window.js"},
        {id: "text_box", src: "./text_box.js"},
        {id: "colon_line", src: "./colon_line.js"},
        {id: "status_line", src: "./status_line.js"},
        {id: "client", src: "./client.js"},
        {id: "viewport", src: "./viewport.js"},
        {id: "map", src: "./map.js"}
    ]);
}


function init(){


    while(cursed.state.username == ""){
        cursed.state.username = window.prompt("Please enter a username.", "");
    }
    while(cursed.state.password == ""){
        cursed.state.password = window.prompt("Please enter session password.", "");
    }
    

    set_canvas_size();
    stage = new createjs.Stage("canvas");
    build_namespace();
    init_modules();

    cursed.viewport.draw();
    cursed.command_window.draw();
    cursed.text_box.draw();
    cursed.colon_line.draw();
    cursed.status_line.draw();

    document.onkeydown = handleKeypress;

    // global draw loop
    createjs.Ticker.framerate = 60;
    createjs.Ticker.addEventListener("tick", ()=>{ 
        if(cursed.viewer.dirty){
            cursed.stage.update(); 

            cursed.viewer.dirty = false;
        }
    });

}

function set_canvas_size(){
    var canvas = document.getElementById("canvas");
    var w = window.innerWidth;
    var h = window.innerHeight;

    canvas.width = w;
    canvas.height = h;

    cursed.constants.grid_width = Math.floor(window.innerWidth/(cursed.constants.font_size + cursed.constants.font_width_offset));

    cursed.constants.grid_height = Math.floor(window.innerHeight/cursed.constants.font_size);

    cursed.constants.width = window.innerWidth;
    cursed.constants.height = window.innerHeight;

    canvas.style.visibility = "visible";
}

function test(){
    var circle = new createjs.Shape();
    circle.graphics.beginFill("Yellow").drawCircle(0, 0, 50);
    circle.x = 200;
    circle.y = 200;

    stage.addChild(circle);
    stage.update();
}

function build_namespace() {
    cursed.stage = stage;
    cursed.features = features;
    cursed.colors = colors;
    cursed.grid = grid;
    cursed.viewport = viewport;
    cursed.command_window = command_window;
    cursed.text_box = text_box; 
    cursed.colon_line = colon_line;
    cursed.status_line = status_line;
    cursed.client = client;
    cursed.map = map;
}

function init_modules(){
    cursed.features.init(); //must be first
    cursed.grid.init(); //must be second

    cursed.viewport.init(); 
    cursed.command_window.init();
    cursed.text_box.init();
    cursed.colon_line.init();
    cursed.status_line.init();
    cursed.map.init()

    // do last
    cursed.client.init();

}

function handleKeypress(e){
    if(!cursed.viewer.handling){
        console.log(e);

        if(cursed.constants.IGNORE.indexOf(e.key) < 0){
            if(cursed.viewer.combo_buffer.length > 0){
                if(e.key === "Escape"){
                    cursed.viewer.combo_buffer = "";
                    cursed.colon_line.clear_buff();
                }

                else if (e.key === "Enter"){
                    if(cursed.viewer.combo_buffer[0] == ":"){
                        var buff = cursed.viewer.combo_buffer.substring(1);
                        
                        if(buff === "save"){
                            //TODO: implement save
                        }
                        else{
                            for(var module of cursed.modules.interactive){
                                module.handle_combo(e);
                            }
                        }
                    
                    }
                    cursed.viewer.combo_buffer = "";
                    cursed.colon_line.clear_buff();
                }

                else if(e.key == "Backspace"){
                    cursed.viewer.combo_buffer = cursed.viewer.combo_buffer.substring(0, cursed.viewer.combo_buffer.length-1);
                    cursed.colon_line.set_buff(cursed.viewer.combo_buffer);
                }
                else{
                    cursed.viewer.combo_buffer += e.key;
                    cursed.colon_line.set_buff(cursed.viewer.combo_buffer);
                }
            }
            else if(cursed.viewer.motion_buffer_count.length > 0){

            }
            else{
                if(e.key === ":"){
                    cursed.viewer.combo_buffer = ":"; 
                    cursed.colon_line.set_buff(":");
                }
                else if (cursed.constants.NUMBERS.indexOf(e.key) >= 0){
                    cursed.viewer.motion_buffer_count += e.key; 
                }
                else{
                    for(var module of cursed.modules.interactive){
                        module.handle(e);                     
                    }
                }
            }
        }

        ////TODO: replace temporary fow toggle
        //if(e.key == "f"){
        //    if(cursed.state.fow === "on"){
        //        cursed.state.fow = "off";
        //        cursed.viewport.dirty = true;
        //        cursed.viewport.clear();
        //        cursed.viewport.draw();
        //    }
        //    else if(cursed.state.fow == "off"){
        //        cursed.state.fow = "on";
        //        cursed.viewport.dirty = true;
        //        cursed.viewport.clear();
        //        cursed.viewport.draw();
        //    }
        //}
    }
}




