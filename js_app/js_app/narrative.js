"use strict";

var narrative = {
    dirty: false,
    showing: false
};

narrative.init = function(){
    cursed.modules.interactive.push(narrative);
    cursed.modules.text_display.push(narrative);

    cursed.client.subscribe("list.narratives", (data)=>{
        var lines = [
            [
                {
                    "text": "Chapters:",
                    "color": "Gold"
                }
            ]
        ]
        
        for(var i=0; i<data.payload.length; i++){
            lines.push([
                {
                    text: ("00" + (i+1)).slice(-2) + ". " + data.payload[i],
                    color: "White"
                }
            ])
        }

        narrative.show();
        cursed.text_box.set(lines);
    });

    cursed.client.subscribe("get.narrative", (data)=>{
        var lines = [];

        var text = data.payload.name + ":\n";
        if(data.payload.text !== null){
            text = data.payload.text
        }
        for(var line of text.split("\n")){
            lines.push([
                {
                    text: line,
                    color: "White"
                }
            ]);
        }

        narrative.show();
        cursed.text_box.set(lines);
    })

    cursed.client.ack("add.narrative", ()=>{
        if(narrative.showing){
            narrative.list();
        }
    });

    cursed.client.ack("remove.narrative", ()=>{
        if(narrative.showing){
            narrative.list();
        }
    });

};

narrative.handle = function(event){

    if(event.key === "n"){
        narrative.show();
        narrative.list();
    }
}

narrative.handle_combo = function(buf){
    buf = buf.split(" ")

    if(buf[0] === "n" || buf[0] === "narrative"){
        
        if(buf[1] === "l" || buf[1] === "list"){
            narrative.list();
        }

        else if((buf [1] === "v" || buf[1] === "view") && buf.length > 2){
            cursed.client.send({
                type: "command",
                key: "get.narrative",
                details: {
                    chapter_no:  parseInt(buf[2])
                }
            });
        }

        else if((buf[1] === "a" || buf[1] === "add") && buf.length > 2){

            var name = buf.slice(2, buf.length).join(" ");
            cursed.client.send({
                type: "command",
                key: "add.narrative",
                details: {
                    name: name
                }
            });
        }
        else if((buf [1] === "r" || buf[1] === "rm" || buf[1] === "remove") && buf.length > 2){
            cursed.client.send({
                type: "command",
                key: "remove.narrative",
                details: {
                    chapter_no: parseInt(buf[2]) 
                }
            });
        }

        else if((buf[1] === "e" || buf[1] === "edit") && buf.length > 2){ // requires a chapter no

            cursed.client.once("get.narrative", (data)=>{
                cursed.viewer.editor_open = true;
                data = data.payload;
                $("#text").val(data.text);
                $("#dialog").dialog({
                    resizable: true,
                    height: "auto",
                    width: "auto",
                    modal: true,
                    buttons: {
                        "Save": function(){
                            $(this).dialog("close");
                            cursed.viewer.editor_open = false;

                            data.text = $("#text").val();
                            cursed.client.send({
                                type: "command",
                                key: "modify.narrative",
                                details: {
                                    chapter_no: parseInt(buf[2]),
                                    name: data.name,
                                    text: data.text
                                }
                            });
                        },
                        "Cancel": function(){
                            $(this).dialog("close");
                        }
                    }
                });
            });

            cursed.client.send({
                type: "command",
                key: "get.narrative",
                details: {
                    chapter_no: parseInt(buf[2])
                }
            });
        }
    }
}

narrative.handle_help = function(buf){

}

narrative.show = function(){
    cursed.modules.text_display.map((e)=>{e.hide();});
    narrative.showing = true;
}

narrative.hide = function(){
    narrative.showing = false;
}

narrative.list = function(){
    narrative.show();
    cursed.client.send({
        type: "command",
        key: "list.narratives"
    });
}
