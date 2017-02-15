"use strict";

var stage;
var queue;
var cursed = {
    constants: {
        font_size: 14,
        font_width_offset: -5,
        font_spacing: -6,
        font_spaced_offset: -0,
        NUMBERS: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        IGNORE: ["Alt", "Ctrl", "Shift"]
    },
    state: {
        username: "",
        password: "",
        fow: "on",
        role: "pc"
    },
    viewer: {
        handling: false,
        dirty : true,
        combo_buffer: "",
        motion_buffer_count: "",
        animation_running: true
    },
    modules: {
        live: [],
        interactive: [],
        text_display: []
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
        {id: "map", src: "./map.js"},
        {id: "users", src: "./users.js"},
        {id: "chat", src: "./chat.js"},
    ]);
}


function init(){

    // Do credential setup

    if(localStorage.username === undefined || localStorage.username == null){
        while(cursed.state.username == ""){
            cursed.state.username = window.prompt("Please enter a username.", "");
            localStorage.username = cursed.state.username;
        }
    }
    else{
        cursed.state.username = localStorage.username;
    }

    if(localStorage.password == undefined || localStorage.password == null){
        while(cursed.state.password == ""){
            cursed.state.password = window.prompt("Please enter session password.", "");
            localStorage.password = cursed.state.password;
        }
    }
    else{
        cursed.state.password = localStorage.password;
    }
    

    // begin preparing the canvas
    set_canvas_size();
    stage = new createjs.Stage("canvas");

    //Begin loading animation
    begin_ani();

    // begin with loading modules
    build_namespace();
    init_modules();

    setTimeout(()=>{
        cursed.viewer.cont_tween.paused = true;
        cursed.viewer.cont_tween.setPaused(true);
        createjs.Tween.get(cursed.viewer.cont).to({alpha:1}, 1000).to({alpha:0}, 1000).call(()=>{
            createjs.Tween.get(cursed.viewer.white_rect).to({alpha:0}, 1000).call(()=>{
                begin_draw();
                begin_keypress();
                cursed.state.animation_running = false;
            });
        });

    }, 5000);


    // global draw loop
    createjs.Ticker.framerate = 60;
    createjs.Ticker.addEventListener("tick", ()=>{ 
        if(cursed.viewer.dirty){
            cursed.stage.update(); 

            if(cursed.state.animation_running){
                cursed.viewer.dirty = false;
            }
        }
    });

}

function begin_ani(){
    var cont = new createjs.Container();
    var rect = new createjs.Graphics.Rect(0, 0, cursed.constants.width, cursed.constants.hight);
    var rect_shape = new createjs.Shape(
        new createjs.Graphics().beginFill("#fff").drawRect(0, 0, cursed.constants.width, cursed.constants.height)
    );
    cursed.viewer.white_rect = rect_shape
    stage.addChild(rect_shape);

    var c = new createjs.Text("C", "120px monospace", "#FFC800"); c.x=0; 
    var u = new createjs.Text("u", "120px monospace", "#FFC800"); u.x=120*1;
    var r = new createjs.Text("r", "120px monospace", "#FFC800"); r.x=120*2;
    var s = new createjs.Text("s", "120px monospace", "#FFC800"); s.x=120*3;
    var e = new createjs.Text("e", "120px monospace", "#FFC800"); e.x=120*4;
    var d = new createjs.Text("d", "120px monospace", "#FFC800"); d.x=120*5;
    var loading = new createjs.Text("Loading...", "40px monospace", "#FFC800"); loading.y=140;
    cont.addChild(c, u, r, s, e, d, loading);
    var bounds = cont.getBounds();
    cont.x = Math.ceil(cursed.constants.width - bounds.width)/2;
    cont.y = 200;
    cont.alpha = 0
    
    var loading_bounds = loading.getBounds();
    loading.x = Math.ceil(bounds.width - loading_bounds.width)/2;

    stage.addChild(cont);
    cursed.viewer.cont = cont;
    
    stage.update();
    cursed.viewer.cont_tween = createjs.Tween.get(cont, {loop: true}).to({alpha: 1}, 2000).to({alpha: 0}, 1000);
}

function begin_draw(){
    // draw initial module graphics
    cursed.grid.ready(); // add grid objects to stage
    cursed.viewport.draw();
    cursed.command_window.draw();
    cursed.text_box.draw();
    cursed.colon_line.draw();
    cursed.status_line.draw();
}

function begin_keypress(){
    // register global key press handler
    document.onkeydown = handleKeypress;
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
    cursed.chat = chat;
    cursed.users = users;
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
    cursed.users.init();
    cursed.chat.init();

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
                            // get buff minus the colon
                            var buff = cursed.viewer.combo_buffer.substring(1, cursed.viewer.combo_buffer.length);
                            for(var module of cursed.modules.interactive){
                                module.handle_combo(buff);
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
