"use strict";

var notes = {
    dirty: false,
    showing: false,
    notes: []
};

notes.init = function(){
    cursed.modules.interactive.push(notes);
    cursed.modules.text_display.push(notes);

    cursed.client.ack("move.user", (data)=>{
        notes.load_notes();
    });

    cursed.client.subscribe("get.map.notes", (data)=>{
        notes.notes = data.payload;
    });


    cursed.client.subscribe("modify.map.note", (data)=>{
        for(var i=0; i<notes.notes.length; i++){
            var note = notes.notes[i];
            if(note.id === data.details.id){
                notes.notes[i] = data.details; 
                break;
            }
        }

        if(notes.showing){ notes.list() }
    });

    cursed.client.subscribe("add.map.note", (data)=>{
        notes.notes.push(data.details);
        notes.list();
    });

    cursed.client.subscribe("remove.map.note", (data)=>{
        var idx = null;

        for(var i=0; i<notes.notes.length; i++){
            var note = notes.notes[i];
            if(note.id == data.details.id){
                idx = i;
                break;
            }
        }

        if(idx === null){ return; }

        notes.notes.splice(idx, 1);

        notes.list();
        
        //redraw to rm note
        cursed.viewport.dirty = true; 
        cursed.viewport.draw();
    });

    cursed.client.registerInitHook(()=>{
        notes.load_notes();
    });
}

notes.show = function(){
    cursed.modules.text_display.map((e)=>{e.hide();});
    notes.showing = true;
}

notes.hide = function(){
    notes.showing = false;
}

notes.handle = function(e){
    if(command_window.mode === command_window.command_modes.default){
        if(e.key === "N"){
            notes.list()
        }
    }
}

notes.handle_combo = function(buff){
    buff = buff.split(" ");
    if(buff[0] === "no" || buff[0] === "notes" || buff[0] === "note"){

        if(buff[1] == "add" || buff[1] == "a" || buff[1] == "new"){
            var name = buff.slice(2, buff.length).join(" ");
            notes.add(name);
        }
        else if(buff[1] == "rm" || buff[1] == "r"){
            var name = buff.slice(2, buff.length).join(" ");
            notes.remove(name);
        }
        else if(buff[1] == "list" || buff[1] == "l"){
            notes.list(); 
        }
        else if(buff[1] == "view" || buff[1] == "v"){
            var name = buff.slice(2, buff.length).join(" ");
            notes.view(name); 
        }
        else if(buff[1] == "edit" || buff[1] == "e"){
            var name = buff.slice(2, buff.length).join(" ");
            notes.edit(name);
        }
    }
}

notes.handle_help = function(buf){

}

notes.list = function(){
    notes.show();

    var lines = [
        [{
                text: "Notes: ",
                color: "Gold"
        }]
    ];


    if(notes.notes.length > 0){
        for(var note of notes.notes){
            lines.push([
                {
                    text: "- " + note.name + ": ",
                    color: "Light Grey"
                },
                {
                    text: note.text.substring(0, 100),
                    color: "White"
                }
            ]);
        }
    }
    else {
        lines.push([
            {
                text: "No notes yet. Try ':notes add [note name]' to add a new note.",
                color: "Dark Grey"
            }
        ]);
    }

    cursed.text_box.set(lines);
}

notes.add = function(name){

    cursed.client.send({
        type: "command",
        key: "add.map.note",
        details: {
            "name": name,
            "text": "",
            "x": viewport.cursor_x + viewport.v_x,
            "y": viewport.cursor_y + viewport.v_y,
            "id": Math.random().toString(36).substring(7)
        }
    }, true);
}

notes.remove = function(name){
    var id = null;

    for(var note of notes.notes){
        if(note.name === name){
            id = note.id;
            break;
        }
    }

    if(id === null){
        return;
    }

    cursed.client.send({
        type: "command",
        key: "remove.map.note",
        details: {
            "id": id
        }
    }, true);
    
}

notes.edit = function(name){
    var edit_note = null;

    for(var note of notes.notes){
        if(note.name === name){
            edit_note= note;
            break;
        }
    }

    if(edit_note === null){
        return;
    }

    $("#text").val(edit_note.text);
    $("#dialog").dialog({
        resizable: true,
        height: "auto",
        width: "auto",
        modal: true,
        open: function(){
            // pause keypress handling
            cursed.viewer.editor_open = true;               
        },
        close: function(){
            // allow client to handle keypresses again
            cursed.viewer.editor_open = false;               
        },
        buttons: {
            "Save": function(){

                var text = $("#text").val();
                cursed.client.send({
                    type: "command",
                    key: "modify.map.note",
                    details: {
                        "id": edit_note.id,
                        "name": edit_note.name,
                        "text": text,
                        "x": edit_note.x,
                        "y": edit_note.y
                    }
                }, true);

                $(this).dialog("close");
            },
            "Cancel": function(){
                $(this).dialog("close");
            }
        }
    });
}

notes.view = function(name){

    var view_note = null;

    for(var note of notes.notes){
        if(note.name === name){
            view_note = note;
            break;
        }
    }

    if(view_note === null){
        return;
    }

    notes.show();

    cursed.text_box.set([
        [
            {
                text: view_note.name + ": ",
                color: "Gold"
            }
        ],
        [
            {
                text: view_note.text,
                color: "White"
            }
        ]
    ]);
}

notes.load_notes = function(){
    cursed.client.send({
        type: "command",
        key: "get.map.notes"
    });
}
