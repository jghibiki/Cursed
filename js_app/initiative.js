
var initiative = {
    dirty: false,
    units: [],
    text: [ [{text: "Units in Encounter:", color: "Gold" }] ],
    encounter_started: false,
    showing: false
};


initiative.init = function(){

}

initiative.addUnit = function(){
    if(!initiative.encounter_started){
        var unit = cursed.viewport.getCurrentUnit();
        if(unit !== null){
            for(var i=0; i<initiative.units.length; i++){
                if(initiative.units[i].id == unit.id){
                    return;
                }
            }
            

            initiative.units.push({
                id: unit.id,
                name: unit.name,
                type: unit.type,
                x: unit.x,
                y: unit.y,

                initiative: 0,
                roll: 0,
                modifier: 0,
                selected: initiative.units.length === 0
            });
            initiative.updateText();
        }
    }
}


initiative.removeUnit = function(){
    if(!initiative.encounter_started){
        var unit = cursed.viewport.getCurrentUnit();
        if(unit !== null){
            for(var i=0; i<initiative.units.length; i++){
                if(initiative.units[i].id == unit.id){
                    var selected = initiative.units[i].selected;
                    initiative.units.splice(i, 1);

                    if(selected && initiative.units.length > 0){
                        if(i > 0){
                            initiative.units[i-1].selected = selected;
                        }
                        else if(i === 0 && initiative.units.length > 1){
                            initiative.units[i+1].selected = selected;
                        }
                        else if(i === 0 && initiative.units.length === 1){
                            initiative.units[i].selected = selected;
                        }
                    }

                    initiative.updateText();
                    return;
                }
            }
        }
    }
}

initiative.beginEncounter = function(){
    initiative.encounter_started = true;

    //roll initiative
    for(var i=0; i<initiative.units.length; i++){
        initiative.units[i].selected = false;

        initiative.units[i].roll = Math.floor(Math.random() * cursed.state.initiative_die_sides);
        initiative.units[i].initiative = initiative.units[i].roll + initiative.units[i].modifier;
    }

    if(initiative.units.length > 0){
        initiative.units[0].selected = true;
    }
    
    initiative.updateText();
};

initiative.endEncounter = function(){
    initiative.encounter_started = false;
    initiative.updateText();
};

initiative.show = function(){
    // hide all modules
    cursed.modules.text_display.map((e)=>{e.hide();});
    //show initiative
    initiative.showing = true;
    cursed.text_box.set(initiative.text);
};

initiative.updateText = function(){
    var lines = [ [{
        text: "Units in Encounter:",
        color: "Gold"
    }] ];

    initiative.units = initiative.units.sort((a,b)=>{ return b.initiative-a.initiative; });

    for(var unit of initiative.units){
        var color = null;
        if(unit.type === "enemy"){
            color = "Dark Red";
        }
        else if(unit.type === "neutral"){
            color = "Grey";
        }
        else if(unit.type === "pc"){
            color = "Light Green";
        }

        var marker = " ";
        if(unit.selected){ marker = ">"; }

        var order = "  ";
        if(initiative.encounter_started){
            //padded initiative value
            order = ("  " + unit.initiative.toString()).slice(-2);
        }

        lines.push([
            {
                text: marker + " ",
                color: "Gold"
            },
            {
                text: order,
                color: "White"
            },
            {
                text: unit.name,
                color: color
            },
            {
                text: "(x:" + unit.x.toString() + ", y:" + unit.y.toString() + ")",
                color: "Dark Grey"
            }
        ]);
    }

    initiative.text = lines;

    if(initiative.showing){
        cursed.text_box.set(lines);        
    }
}

initiative.selectNext = function(){
    for(var i=0; i<initiative.units.length; i++){
        var selected = initiative.units[i].selected;
        initiative.units[i].selected = false;

        if(!selected){ continue; } // skip the rest of this iteration
        
        if(initiative.units.length-1 > i){
            initiative.units[i+1].selected = true;
            initiative.updateText();
            return;
        }
        else if(initiative.units.length-1 === i){
            initiative.units[0].selected = true ;
            initiative.updateText();
            return;
        }
    }

}

initiative.selectPrevious = function(){
    for(var i=0; i<initiative.units.length; i++){
        var selected = initiative.units[i].selected;
        initiative.units[i].selected = false;
        
        if(!selected){ continue; } // skip the rest of this iteration
        
        if(i === 0){
            initiative.units[initiative.units.length-1].selected = true ;
            initiative.updateText();
            return;
        }
        else{
            initiative.units[i-1].selected = true ;
            initiative.updateText();
            return;
        }
    }
}
