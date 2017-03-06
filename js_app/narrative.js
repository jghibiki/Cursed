"use strict";

var narrative = {
    dirty: false,
    showing: false
};

narrative.init = function(){
    cursed.modules.interactive.push(narrative);
    cursed.modules.text_display.push(narrative);

};

narrative.handle = function(event){

    if(event.key === "n"){
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
            var url = "/narrative/" + (parseInt(buf[2]) - 1);
            cursed.client.request(url, null, (data)=>{
                var lines = [];

                for(var line of data.text.split("\n")){
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
        }

        else if((buf[1] === "a" || buf[1] === "add") && buf.length > 2){

            var name = buf.slice(2, buf.length).join(" ");
            cursed.client.request("/narrative", { name: name}, ()=>{
                narrative.list();
            });
        }
        else if((buf [1] === "r" || buf[1] === "rm" || buf[1] === "remove") && buf.length > 2){
            var url = "/narrative/delete/" + (parseInt(buf[2]) - 1);
            cursed.client.request(url, null, (data)=>{
                narrative.list();
            });
        }

        else if((buf[1] === "e" || buf[1] === "edit") && buf.length > 2){ // requires a chapter no
            var url = "/narrative/" + (parseInt(buf[2]) - 1);
            cursed.client.request(url, null, (data)=>{

                cursed.viewer.editor_open = true;
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
                            var url = "/narrative/" + (parseInt(buf[2]) - 1);
                            cursed.client.request(url, data, ()=>{
                                narrative.list(); 
                            });
                        },
                        "Cancel": function(){
                            $(this).dialog("close");
                        }
                    }
                });
            });
        }
    }
}

narrative.handle_help = function(buf){

}

narrative.show = function(){
    narrative.showing = true;
    cursed.modules.text_display.map((e)=>{e.hide();});
}

narrative.hide = function(){
    narrative.showing = false;
}

narrative.list = function(){
    narrative.show();
    cursed.client.request("/narrative", null, (data)=>{
        var lines = [
            [
                {
                    "text": "Chapters:",
                    "color": "Gold"
                }
            ]
        ]
        
        for(var i=0; i<data.chapters.length; i++){
            lines.push([
                {
                    text: ("00" + (i+1)).slice(-2) + ". " + data.chapters[i],
                    color: "White"
                }
            ])
        }

        narrative.show();
        cursed.text_box.set(lines);
    });
}
