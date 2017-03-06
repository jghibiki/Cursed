"use strict";

var features = {};

features.objects = [
    {
        name: "Wall",
        character: "\u2588",
        color: "Brown"
    },
    {
        name: "Table",
        character: "T",
        color: "Brown"
    },
    {
        name: "Chair",
        character: "c",
        color: "Brown"
    },
    {
        name: "Door",
        character: "d",
        color: "Brown"
    },
    {
        name: "Up Stair",
        character: "\u2191",
        color: "Brown"
    },
    {
        name: "Down Stair",
        character: "\u2193",
        color: "Brown"
    },
    {
        name: "Lantern",
        character: "%",
        color: "Gold"
    },
    {
        name: "Road",
        character: "\u2588",
        color: "Grey"
    },
    {
        name: "Chest",
        character: "#",
        color: "White"
    },
    {
        name: "Gate",
        character: "G",
        color: "Brown"
    },
    {
        name: "Water",
        character: "~",
        color: "Light Blue"
    },
    {
        name: "Tree",
        character: "O",
        color: "Brown"
    },
    {
        name: "Bush",
        character: "o",
        color: "Dark Green"
    },
    {
        name: "Grass",
        character: ".",
        color: "Dark Green"
    },
    {
        name: "Hill",
        character: "^",
        color: "White"
    },
    {
        name: "Bed",
        character: "b",
        color: "Brown"
    },
    {
        name: "Statue",
        character: "&",
        color: "White"
    },
    {
        name: "Blood",
        character: "\u2588",
        color: "Dark Red"
    },
    {
        name: "Fire",
        character: "~",
        color: "Orange"
    },
    {
        name: "Snow",
        character: "\u2588",
        color: "White"
    },
    {
        name: "Boulder",
        character: "O",
        color: "Dark Grey"
    }
];


features.init = function(){
}

features.test = function(){
    var x = 0;
    var y = 0;
    var texts = [];

    var max = 20;

    for(let feature of features.objects){
        var text = new createjs.Text(feature.character, "20px monospace", feature.color.value);
        var h =  text.getMeasuredHeight();
        if(h > max){ max = h; }
        texts.push(text);
    }

    for(let text of texts){
        text.x = x;
        text.y = y;
        stage.addChild(text);
        y = y + max;
    }
    stage.update();
}



features.new = function(feature_name, x, y){
    var new_feature = null;
    for(feature of feature.objects){
        if(feature.name == feature_name){
            new_feature = feature;
        }
    }

    if(new_feature !== null){
        var text = new createjs.Text(new_feature.character, "20px monospace", new_feature.color.value);
        text.x = x;
        text.y = y;
        return text;
    }
    return null;
}

features.get = function(name){
    for(var feature of features.objects){
        if(feature.name == name){
            return feature;
        }
    }
}
