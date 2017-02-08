
var grid = {};

grid.init = function(){
    var builder = new createjs.SpriteSheetBuilder();  

    var characters = [ 
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
        "\u2588", // block character
        "\u2191", // up arrow character
        "\u2193", // down arrow character
        "~", "^", "#", "!", "@", "&", ".", ":",
        " "
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
    
    
    
    var width = Math.ceil(cursed.constants.grid_width/2);
    var height = Math.floor(Math.floor((cursed.constants.height - (3 * cursed.constants.font_size))) / cursed.constants.font_size);


    var grid_x = Math.ceil(cursed.constants.grid_width/3) * (cursed.constants.font_size + cursed.constants.font_width_offset);
    var grid_y = 0;

    var canvas = document.getElementById("canvas");
    grid._ = new Array(height);
    for(var i=0; i<height; i++){
        grid._[i] = new Array(width);
        for(var j=0; j<width; j++){

            var x = (j * (cursed.constants.font_size -5)) + grid_x;
            var y = (i * cursed.constants.font_size) + grid_y;

            var text = new createjs.BitmapText("A", cursed.ss);
            text.x = x;
            text.y = y;

            var bounds = text.getBounds();
            var w = bounds.width;
            var h = bounds.height;
            text.cache(0, 0, w*2, h*2);

            stage.addChild(text);

            grid._[i][j] = text;
        }
    }
    stage.update();
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
