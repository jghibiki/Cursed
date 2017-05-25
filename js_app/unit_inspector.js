"use strict";

var unit_inspector = {
    dirty: false,
    showing: false
};

unit_inspector.init = function(){
    cursed.modules.interactive.push(unit_inspector);
    cursed.modules.text_display.push(unit_inspector);
}

unit_inspector.show = function(){
    if(!unit_inspector.showing){
        
        var unit = cursed.viewport.getCurrentUnit();
        if(unit === null){ return; }

        cursed.modules.text_display.map((e)=>{e.hide();});
        unit_inspector.showing = true;

        var lines = unit_inspector.build_lines(unit);
        cursed.text_box.set(lines);
    }
}

unit_inspector.hide = function(){
    unit_inspector.showing = false;
}

unit_inspector.handle = function(e){

}

unit_inspector.handle_combo = function(buf){

}

unit_inspector.handle_help = function(buf){

}

unit_inspector.build_lines = function(unit){
    var lines = [
        [
            {
                "text": unit.name + ":",
                "color": "Gold"
            }
        ],
        [
            {
                "text": "Health: ",
                "color": "Light Green"
            },
            {
                "text": unit.current_health + "/" +unit.max_health,
                "color": "White"
            }
        ],
        [
            {
                "text": "Controller: ",
                "color": "Light Green"
            },
            {
                "text": unit.controller,
                "color": "White"
            }
        ],
        [
            {
                "text": "Unit Type: ",
                "color": "Light Green"
            },
            {
                "text": unit.type,
                "color": "White"
            }
        ]
    ]

    if(unit.template_type !== null){
        lines.push([
            {
                "text": "User-defined Unit Type",
                "color": "Light Green"
            },
            {
                "text": unit.template_type,
                "color": "White"
            }
        ]);
    }

    for(var field of unit.template_values){
        var field_line = [
            {
                "text": field.label + ": ",
                "color": "Light Blue"
            }
        ];

        var splits = field.value.split("\n");
        var first_line = true;
        for(var split of splits){
            if(split !== ""){
                if (first_line){
                    field_line.push(
                        {
                            "text": split,
                            "color": "White"
                        }
                    );
                    lines.push(field_line);
                    first_line = false;
                }
                else{
                    lines.push([
                        {
                            "text": split,
                            "color": "White"
                        }
                    ]);
                }
            }
        };
    }

    return lines;
}
