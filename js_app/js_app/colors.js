"use strict";

var colors = {};


colors.objects = [
    {
        name: "Light Red",
        r: 255,
        g: 118,
        b: 118,
        value: "#FF7676"
    },
    {
        name: "Red",
        r: 255,
        g: 0,
        b: 0,
        value: "#FF0000"
    },
    {
        name: "Dark Red",
        r: 133,
        g: 0,
        b: 0,
        value: "#850000"
    },

    {
        name: "Light Green",
        r: 118,
        g: 255,
        b: 118,
        value: "#76FF76"
    },
    {
        name: "Green",
        r: 0,
        g: 255,
        b: 0,
        value: "#00FF00"
    },
    {
        name: "Dark Green",
        r: 0,
        g: 133,
        b: 0,
        value: "#008500"
    },

    {
        name: "Light Blue",
        r: 118,
        g: 118,
        b: 255,
        value: "#7676FF"
    },
    {
        name: "Blue",
        r: 0,
        g: 0,
        b: 255,
        value: "#0000FF"
    },
    {
        name: "Dark Blue",
        r: 0,
        g: 0,
        b: 133,
        value: "#000085"
    },

    {
        name: "Light Grey",
        r: 200, 
        g: 200, 
        b: 200,
        value: "#C8C8C8"
    },
    {
        name: "Grey",
        r: 138, 
        g: 138, 
        b: 138,
        value: "#8A8A8A"
    },
    {
        name: "Dark Grey",
        r: 94, 
        g: 94, 
        b: 94,
        value: "#5E5E5E"
    },


    {
        name: "Brown",
        r: 145, 
        g: 73, 
        b: 0,
        value: "#914900"
    },


    {
        name: "Gold",
        r: 255, 
        g: 200, 
        b: 0,
        value: "#FFC800"
    },

    {
        name: "Orange",
        r: 255, 
        g: 150, 
        b: 0,
        value: "#FF9600"
    },
    {
        name: "White",
        r: 255, 
        g: 255, 
        b: 255,
        value: "#ffffff"
    }
];

colors.get = function(name){
    for(var color of cursed.colors.objects){
        if(color.name === name){
            return color
        }
    }
    return null
};
