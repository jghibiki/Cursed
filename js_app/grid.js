
var grid = {};

grid.init = function(){
    var builder = new createjs.SpriteSheetBuilder();  

    var characters = [ 
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
        "\u2588", // block character
        "\u2588", // up arrow character
        "\u2588", // down arrow character
        " "
    ];

    var char_map = {};

    for(var c of characters){
        var text = new createjs.Text(c, cursed.constants.font_size + "px monospace", "#fff");
        
        char_map[c] = builder.addFrame(text);
        builder.addAnimation(c, char_map[c]);
    }

    grid.ss = builder.build();


    var bit_text = new createjs.BitmapText("Test", grid.ssss);
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

            var text = new createjs.BitmapText("A", grid.ss);
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

    grid._[y][x].text = text;
    grid._[y][x].color = cursed.colors.get(color).value;
    grid._[y][x].updateCache();

}
