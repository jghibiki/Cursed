"use strict";

var notes = {
    dirty: false,
    showing: false
};

notes.init = function(){
    cursed.modules.interactive.push(notes);
    cursed.modules.text_display.push(notes);
}

notes.show = function(){
    cursed.modules.text_display.map((e)=>{e.hide();});
    notes.showing = true;
}

notes.hide = function(){
    notes.showing = false;
}

notes.handle = function(e){

}

notes.handle_combo = function(buf){

}

notes.handle_help = function(buf){

}
