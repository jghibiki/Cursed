
var grid = {};

grid.init = function(){
    var builder = new createjs.SpriteSheetBuilder();  
    builder.padding = 3;

    var characters = [ 
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
        "\u2588", // block character
        "\u2191", // up arrow character
        "\u2193", // down arrow character
        "~", "^", "#", "!", "@", "&", ".", ":", "_", "/", "|", "\\", "+", "-", "[", "]", "(", ")", "<", ">", "=", "+", " ", "-", "#", "%", "*",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
    ];

    var char_map = {};

    for(var c of characters){
        var text = new createjs.Text(c, cursed.constants.font_size + "px monospace", "#fff");
        
        char_map[c] = builder.addFrame(text);
        builder.addAnimation(c, char_map[c]);
    }

    cursed.ss = builder.build();


    var bit_text = new createjs.BitmapText("Test", cursed.ss);
    //bit_text.x = 100;
    //bit_text.y = 100;
    //stage.addChild(bit_text);
    //stage.update();
    
    
    
    grid.width = Math.floor(cursed.constants.grid_width/2);
    grid.height = Math.floor(
        (cursed.constants.height - (3 * (cursed.constants.font_size+2))) //remove 3 lines from bottom of screen
        / (cursed.constants.font_size+2)); //get number of lines -3 


    var grid_x = Math.floor(cursed.constants.grid_width/3) * (cursed.constants.font_size + cursed.constants.font_width_offset) + 2;
    var grid_y = 0;

    var canvas = document.getElementById("canvas");
    grid._ = new Array(grid.height);
    for(var i=0; i<grid.height; i++){
        grid._[i] = new Array(grid.width);
        for(var j=0; j<grid.width; j++){

            var x = (j * (cursed.constants.font_size + cursed.constants.font_width_offset)) + grid_x;
            var y = (i * (cursed.constants.font_size+2)) + grid_y;

            var text = new createjs.BitmapText("A", cursed.ss);
            text.x = x;
            text.y = y;

            var bounds = text.getBounds();
            var w = bounds.width;
            var h = bounds.height;
            text.cache(0, 0, w*2, h*2);


            grid._[i][j] = text;
        }
    }
    stage.update();
}

grid.ready = function(){
    for(var row of grid._){
        for(var ch of row){
            stage.addChild(ch);
        }
    }

}

grid.draw = function(){
    for(var i=0; i<grid._length; i++){
    }

};

grid.text = function(y, x, text, color){
    if(color === null || color === undefined){
        color = "White";
    }

    var color_obj = cursed.colors.get(color);


    var update_text = true;
    var current_text = grid._[y][x].text;

    if(grid._[y][x].filters !== null){
        var current_red = grid._[y][x].filters[0].redOffset;
        var current_green = grid._[y][x].filters[0].greenOffset;
        var current_blue = grid._[y][x].filters[0].blueOffset;

        update_text = (
            current_text !== text ||
            (current_red !== color_obj.r || current_red === undefined) ||
            (current_green !== color_obj.g || current_green === undefined) ||
            (current_blue !== color_obj.b || current_blue == undefined) 
        );
    }

    if(update_text){
        grid._[y][x].text = text;
        grid._[y][x].filters = [
            new createjs.ColorFilter(0, 0, 0, 1, color_obj.r, color_obj.g, color_obj.b, 0)
        ];
        grid._[y][x].updateCache();
    }

}
