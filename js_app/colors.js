"use strict";

var colors = {};


colors.objects = [
    {
        name: "Light Red",
        value: "#FF7676"
    },
    {
        name: "Red",
        value: "#FF0000"
    },
    {
        name: "Dark Red",
        value: "#850000"
    },

    {
        name: "Light Green",
        value: "#76FF76"
    },
    {
        name: "Green",
        value: "#00FF00"
    },
    {
        name: "Dark Green",
        value: "#008500"
    },

    {
        name: "Light Blue",
        value: "#7676FF"
    },
    {
        name: "Blue",
        value: "#0000FF"
    },
    {
        name: "Dark Blue",
        value: "#000085"
    },

    {
        name: "Light Grey",
        value: "#C8C8C8"
    },
    {
        name: "Grey",
        value: "#8A8A8A"
    },
    {
        name: "Dark Grey",
        value: "#5E5E5E"
    },


    {
        name: "Brown",
        value: "#914900"
    },


    {
        name: "Gold",
        value: "#FFC800"
    },

    {
        name: "Orange",
        value: "#FF9600"
    },
    {
        name: "White",
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
