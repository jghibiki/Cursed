
var map = {
    map_hash: null,
    fow_hash: null,
    unit_hash: null,
    note_hash: null
};

map.init = function(){
    cursed.modules.live.push(map);
    cursed.modules.interactive.push(map);
}

map.update = function(hashes){
    var update = false;

    var map_hash = hashes["map"]
    if(map_hash !== map.map_hash){
        map.map_hash = map_hash;
        
        cursed.client.request("/map/data/", null, (data)=>{
            cursed.viewport.updateBounds(data["max_x"], data["max_y"]);
            cursed.viewport.updateFeatures(data["features"]);
        });
    }

    var fow_hash = hashes["fow"];
    if(fow_hash !== map.fow_hash){
        map.fow_hash = fow_hash;

        cursed.client.request("/fow", null, (data)=>{
            cursed.viewport.updateFow(data["fow"]);
        });

    }

    var unit_hash = hashes["unit"];
    if(unit_hash !== map.unit_hash){
        map.unit_hash = unit_hash;

        cursed.client.request("/unit", null, (data)=>{
            cursed.viewport.updateUnits(data["units"]);
        });
    }

}

map.handle = function(e){
    if(e.key == "f"){
        if(cursed.state.fow === "on"){
            cursed.state.fow = "off";
            cursed.viewport.dirty = true;
            cursed.viewport.clear();
            cursed.viewport.draw();
        }
        else if(cursed.state.fow == "off"){
            cursed.state.fow = "on";
            cursed.viewport.dirty = true;
            cursed.viewport.clear();
            cursed.viewport.draw();
        }
    }
};

map.handle_combo = function(e){

}
