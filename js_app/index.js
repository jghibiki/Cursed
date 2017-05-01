"use strict";

var stage;
var queue;
var cursed = {
    constants: {
        font_size: 14,
        font_width_offset: -6,
        font_spacing: -6,
        font_spacing_offset: -0,
        NUMBERS: ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        IGNORE: ["Alt", "Ctrl", "Shift"]
    },
    state: {
        username: "",
        password: "",
        server_ip: "",
        server_port: "",
        fow: "on",
        role: "pc",
        move_mode: "hjkl",
        initiative_die_sides: 20
    },
    viewer: {
        handling: false,
        dirty : true,
        combo_buffer: "",
        motion_buffer_count: "",
        animation_running: true,
        editor_open: false
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
        {id: "features", src: "./features.js"},
        {id: "colors", src: "./colors.js"},
        {id: "grid", src: "./grid.js"},
        {id: "command_window", src: "./command_window.js"},
        {id: "text_box", src: "./text_box.js"},
        {id: "colon_line", src: "./colon_line.js"},
        {id: "status_line", src: "./status_line.js"},
        {id: "client", src: "./new_client.js"},
        {id: "viewport", src: "./viewport.js"},
        {id: "map", src: "./map.js"},
        {id: "users", src: "./users.js"},
        {id: "chat", src: "./chat.js"},
        {id: "narrative", src: "./narrative.js"},
        {id: "roll", src: "./roll.js"},
        {id: "initiative", src: "./initiative.js"},
        {id: "feature_packs", src: "./feature_packs.json"}
    ]);
}


function init(){

    // Do credential setup
    cxnCredentials();

    // begin preparing the canvas
    set_canvas_size();
    stage = new createjs.Stage("canvas");
    cursed.stage = stage;

    if(localStorage.loading_screen !== undefined && localStorage.loading_screen == "true"){
        //
        //Begin loading animation
        begin_ani();

        // begin with loading modules

        setTimeout(()=>{
            cursed.viewer.cont_tween.paused = true;
            cursed.viewer.cont_tween.setPaused(true);

            createjs.Tween.get(cursed.viewer.cont).to({alpha:1}, 1000).call(()=>{

                build_namespace();
                init_modules();

                createjs.Tween.get(cursed.viewer.cont).wait(500).to({alpha:0}, 1000).wait(200).call(()=>{
                    createjs.Tween.get(cursed.viewer.white_rect).to({alpha:0}, 1000).call(()=>{
                        begin_draw();
                        begin_keypress();
                        cursed.viewer.animation_running = false;
                    });
                })
            });

        }, 5000);
    }
    else{
        cursed.viewer.animation_running = false;
        if(localStorage.loading_screen === undefined){
            localStorage.loading_screen = true;
        }
        build_namespace();

        //save handler
        cursed.client.subscribe("save", ()=>{console.log("Game Saved");});

        init_modules();
        begin_draw();
        begin_keypress();
    }


    // global draw loop
    createjs.Ticker.framerate = 60;
    createjs.Ticker.addEventListener("tick", ()=>{ 
        if(cursed.viewer.dirty || cursed.viewer.animation_running){
            cursed.stage.update(); 
            console.log("stage updated");
            cursed.viewer.dirty = false;
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

    var c = new createjs.Text("C u r s e d", "120px monospace", "#FFC800"); c.x=0; 
    var loading = new createjs.Text("Loading...", "40px monospace", "#FFC800"); loading.y=140;
    cont.addChild(c, loading);
    var bounds = cont.getBounds();
    cont.x = Math.ceil(cursed.constants.width - bounds.width)/2;
    cont.y = 200;
    cont.alpha = 0
    
    var loading_bounds = loading.getBounds();
    loading.x = Math.ceil(bounds.width - loading_bounds.width)/2;

    bounds = cont.getBounds();
    cont.cache(0, 0, bounds.width*2, bounds.height*2);

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

    cursed.constants.grid_height = Math.floor(window.innerHeight/(cursed.constants.font_size+2));

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
    cursed.features = features;
    cursed.features.packs = queue.getResult("feature_packs").feature_packs;
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
    cursed.narrative = narrative;
    cursed.roll = roll;
    cursed.initiative = initiative;
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
    cursed.narrative.init();
    cursed.roll.init();
    cursed.initiative.init();

    // do last
    cursed.client.init();

}

function handleKeypress(e){
    if(!cursed.viewer.handling && !cursed.viewer.editor_open){

        e.stopPropagation();

        if(cursed.constants.IGNORE.indexOf(e.key) < 0){

            if(cursed.viewer.combo_buffer.length > 0){
                if(e.key === "Escape"){
                    cursed.viewer.combo_buffer = "";
                    cursed.colon_line.clear_buff();
                }

                else if (e.key === "Enter"){
                    if(cursed.viewer.combo_buffer[0] == ":"){
                        var buff = cursed.viewer.combo_buffer.substring(1);
                        var split = buff.split(" ")
                        
                        if(buff === "save" || buff == "w"){
                            console.log("Saving...");
                            cursed.client.send({ type: "command", key: "save"})
                        }
                        else if(buff == "ls"){
                            localStorage.loading_screen = !(localStorage.loading_screen == "true");
                        }
                        else if(buff == "reset"){
                            localStorage.clear();
                        }
                        else if(split[0] === "set" && split.length > 2){
                            var var_name = split[1];
                            var var_value = split.slice(2, split.length).join(" ");
                            if(var_name === "server_ip" || var_name === "server_port" || var_name === "username" || var_name === "password"){
                                localStorage.setItem(var_name, var_value);                      
                                cursed.state[var_name] = var_value;
                            }
                            else if(var_name === "move_mode"){ // verify valid move_mode settings
                                if(var_value === "hjkl" || var_value === "ijkl"){
                                    localStorage.setItem(var_name, var_value);                      
                                    cursed.state[var_name] = var_value;
                                }
                            }
                            else{
                                cursed.state[var_name] = var_value;
                            }
                        }
                        else if(buff === "help"){
                            e.preventDefault(); // prevents propogation of enter keypress to done
                            var el = $("#help_dialog");
                            el.prop("title", "Help Overview");

                            var content = $("#help_content");
                            content.html(`
                                <p>
                                    Cursed is a very complex system with lots of very powerful (but not evident) features. This help overview is intended to confortable with using the Cursed help system and will aid you in viewing other help articles about the various facets of Cursed.
                                </p>
                                <br>

                                <b><u>Interface:</u></b>
                                <p>
                                    The interface is broken up into five major regions. The text box (left), the map viewer (center), the command window (right), the colon line (bottom left), and the status line (bottom right). The help articles for each of these sections can be viewed by first typing colon to enter colon mode and then any of the following: 
                                    <pre>help text box</pre>
                                    <pre>help map viewer</pre>
                                    <pre>help command window</pre>
                                    <pre>help colon line</pre>
                                    <pre>help status line</pre>
                                    <br>

                                    Reading these help articles will explain how each section of the interface works togeather. Additionally you can view the following help articles for more advanced features:
                                    <pre>help reset</pre>
                                    <pre>help set</pre>
                                    <pre>help chat</pre>
                                    <pre>help fow</pre>
                                    <pre>help build</pre>
                                    <pre>help units</pre>
                                    <pre>help narrative</pre>
                                    <pre>help gm</pre>
                                    <pre>help pc</pre>
                                    <pre>help move_mode</pre>
                                </p>
                            `);
                            el.dialog({
                                resizable: true,
                                height: "auto",
                                width: "75%",
                                modal: true,
                                open: function(){
                                    // pause keypress handling
                                    cursed.viewer.editor_open = true;               
                                    $("#help_dialog").blur();
                                },
                                close: function(){
                                    // allow client to handle keypresses again
                                    cursed.viewer.editor_open = false;               
                                },
                                buttons: {
                                    "Close": function(){
                                        $(this).dialog("close");
                                    }
                                }
                            });

                        }
                        else if(split[0] === "help" && split.length > 1){
                            var help_buff = split.splice(1, split.length).join(" ");
                            e.preventDefault(); // prevents propogation of enter keypress to done
                            for(var module of cursed.modules.interactive){
                                module.handle_help(help_buff);
                            }
                        }
                        else{
                            // get buff minus the colon
                            for(var module of cursed.modules.interactive){
                                module.handle_combo(buff);
                            }
                            e.preventDefault();
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
    }
}

function cxnCredentials(){
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
    
    if(localStorage.server_ip == undefined || localStorage.server_ip == null){
        while(cursed.state.server_ip == ""){
            cursed.state.server_ip = window.prompt("Please enter a Cursed server ip address or hostname (e.g. 192.168.0.X).", "");
            localStorage.server_ip = cursed.state.server_ip;
        }
    }
    else{
        cursed.state.server_ip = localStorage.server_ip;
    }

    if(localStorage.server_port == undefined || localStorage.server_port == null){
        while(cursed.state.server_port == ""){
            cursed.state.server_port = window.prompt("Please enter a Cursed server port number.", "8080");
            localStorage.server_port = cursed.state.server_port;
        }
    }
    else{
        cursed.state.server_port = localStorage.server_port;
    }

    if(localStorage.move_mode == undefined || localStorage.move_mode == null){
        cursed.state.move_mode = "hjkl";
        localStorage.move_mode = "hjkl";
    }
    else{
        cursed.state.move_mode = localStorage.move_mode;
    }
}
