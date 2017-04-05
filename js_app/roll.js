"use strict";

var roll = {
    dirty : false,
    showing: false,
    previous_roll: null
};

roll.init = function(){
    cursed.modules.interactive.push(roll);
    cursed.modules.text_display.push(roll);
};

roll.handle = function(){};

roll.handle_combo = function(buff){
    var split = buff.split(" ");

    if((split[0] === "roll" || split[0] === "r" ) && split.length == 2){
        var text = split[1];
        var log = roll.parse(text);
        roll.previous_roll = text;

        cursed.text_box.set(log);
        narrative.show();
    }

    if((split[0] === "reroll" || split[0] === "rr" )){
        var text = roll.previous_roll;
        if(text !== null){
            var log = roll.parse(text);
            roll.previous_roll = text;

            cursed.text_box.set(log);
            narrative.show();
        }
    }
};

roll.show = function(){
    cursed.modules.text_display.map((e)=>{e.hide();});
    roll.showing = true;
}

roll.hide = function(){
    roll.showing = false;
}

roll.parse = function(text){
    var split 
    var num = 0;
    if(text.indexOf("+") >= 0){
        split = text.split("+");
        try{
            num = parseInt(split[1]);
        }
        catch(e){
            return;
        }
    }
    else if (text.indexOf("-") >= 0){
        split = text.split("-");
        try{
            num = -parseInt(split[1]);
        }
        catch(e){
            return;
        }
    }
    else{
        split = [text];
    }


    var split = split[0].split("d");
    
    var num_dice = split[0];
    var sides = split[1];
    
    var log = [
        [
            {
                "text": "Dice Roller:",
                "color": "Gold"
            }
        ],
        [
            {
                "text": "Rolling " + text,
                "color": "White"
            }
        ]
    ];
    var total = 0;

    for(var i=0; i<num_dice; i++){
        var dice_roll = Math.floor(Math.random() * sides);

        total += dice_roll;
        log.push([
            {
                "text": "Roll #" + i +": " + dice_roll,
                "color": "White"
            }
        ]);
    }

    log.push([
        {
            "text" : "Total: " + ( total + num ),
            "color": "White"
        }
    ]);

    return log;
}

roll.handle_help = function(buff){
    if(buff === "roll"){

        var el = $("#help_dialog");
        el.prop("title", "Help: rolling dice and rerolling dice");

        var content = $("#help_content");
        content.html(`
            <p>
                The roll tool allows players to make dice rolls and view the results in the text box. Rolls take the following format:
                <pre>:roll &lt;number of dice to roll&gt;d&lt;number of sides on die&gt;</pre>

                <br>
                Optionally, you can add or subtract a number to the result:
                <pre>:roll &lt;number of dice to roll&gt;d&lt;number of sides on die&gt;+&lt;number to add&gt;</pre>
                or
                <pre>:roll &lt;number of dice to roll&gt;d&lt;number of sides on die&gt;-&lt;number to subtract&gt;</pre>
                <br>
                Examples:
                <pre>:roll 2d20</pre>
                <pre>:roll 2d6+3</pre>
                <pre>:roll 2d4-1</pre>

                Abbreviated form:
                <pre>:r 2d20</pre>
                <pre>:r 2d6+3</pre>

                <br>
                <hr>
                <br>

                The reroll tool allows you to reroll the last roll that was made. In order to reroll you must have used the roll tool at least once previously. In this browser session.

                Examples:
                <pre>:reroll</pre>

                Abbreviated form:
                <pre>:rr</pre>

            </p>
        `);
        el.dialog({
            resizable: true,
            height: "auto",
            width: "75%",
            modal: true,
            open: function(){
                // pause keypress handling
                cursed.viewer.editor_open = true;               
                $("#help_dialog").blur();
            },
            close: function(){
                // allow client to handle keypresses again
                cursed.viewer.editor_open = false;               
            },
            buttons: {
                "Close": function(){
                    $(this).dialog("close");
                }
            }
        });
    }
}
