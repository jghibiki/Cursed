"use strict";

var viewer = {};

viewer.init = function(){
    
    viewer.x = 0 
    viewer.y = 0;
    viewer.width = Math.ceil(cursed.constants.grid_width/2);
    viewer.height = cursed.constants.grid_height-3;

    viewer.cursor_x = 10;
    viewer.cursor_y = 10;

    // virtual width and height. should be set to map h and w
    viewer.v_height = viewer.height ;
    viewer.v_width = viewer.width; 

}

viewer.draw = function(){

    for(var y=0; y<viewer.height; y++){
        for(var x=0; x<viewer.width; x++){
            
            cursed.grid.text(viewer.y + y, viewer.x + x, " ", "Gold");
        }
    }

    cursed.grid.text(viewer.y + viewer.cursor_y, viewer.x + viewer.cursor_x, "X", "Gold");

    cursed.stage.update();
    
};


viewer.handle = function(event){
    if(event.key === "j"){ viewer.down(); }
    if(event.key === "k"){ viewer.up(); }
    if(event.key === "h"){ viewer.left(); }
    if(event.key === "l"){ viewer.right(); }

}

viewer.up = function(){
    if(viewer.cursor_y > 0){
        cursed.grid.text(viewer.y + viewer.cursor_y, viewer.x + viewer.cursor_x, " ", "Gold");

        viewer.cursor_y -= 1;

        cursed.grid.text(viewer.y + viewer.cursor_y, viewer.x + viewer.cursor_x, "X", "Gold");

        cursed.stage.update();
    }
}

viewer.down = function(){
    if(viewer.cursor_y < viewer.v_height-1){
        cursed.grid.text(viewer.y + viewer.cursor_y, viewer.x + viewer.cursor_x, " ", "Gold");

        viewer.cursor_y += 1;

        cursed.grid.text(viewer.y + viewer.cursor_y, viewer.x + viewer.cursor_x, "X", "Gold");

        cursed.stage.update();
    }
}

viewer.left = function(){
    if(viewer.cursor_x > 0){
        cursed.grid.text(viewer.y + viewer.cursor_y, viewer.x + viewer.cursor_x, " ", "Gold");

        viewer.cursor_x -= 1;

        cursed.grid.text(viewer.y + viewer.cursor_y, viewer.x + viewer.cursor_x, "X", "Gold");

        cursed.stage.update();
    }
}

viewer.right = function(){
    if(viewer.cursor_x < viewer.v_width-1){
        cursed.grid.text(viewer.y + viewer.cursor_y, viewer.x + viewer.cursor_x, " ", "Gold");

        viewer.cursor_x += 1;

        cursed.grid.text(viewer.y + viewer.cursor_y, viewer.x + viewer.cursor_x, "X", "Gold");

        cursed.stage.update();
    }
}
