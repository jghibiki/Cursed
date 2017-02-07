
var map = {
    map_hash: null,
    fow_hash: null,
    unit_hash: null,
    note_hash: null
};

map.init = function(){
    cursed.modules.live.push(map);
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

}


