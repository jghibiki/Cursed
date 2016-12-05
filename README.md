# Cursed
A tool for designing and playing DnD style games via a terminal using the curses library. Supports one Game Master(GM) and multiple Player Characters(PCs). GMs have the power to edit the map and story of the campaign all in one lightweight tool. PCs can then connect to the server to play. The GM has the ability to add and remove Fog of War to obsucre the vision of PCs, add objects to the map and view/edit the campaign narrative all on one screen. 

## Demos: 
### A castle with a coupe of huts out front.
[![asciicast](https://asciinema.org/a/95041.png)](https://asciinema.org/a/95041)

### Editing Notes
Objects with notes are indicated to the GM by flashing. The GM can add/edit the notes attatched to any object. The editor that is used is determined by the ```EDITOR``` environment variable. If ```EDITOR``` is not set, it defaults to ```vim```.

[![asciicast](https://asciinema.org/a/95042.png)](https://asciinema.org/a/95042)

### Narrative

[![asciicast](https://asciinema.org/a/95043.png)](https://asciinema.org/a/95043)

### Chat 
To show the chat window, while on the main command window, press ```c```. To send a message type ```:send <message>``` or ```:s <message>```. To whisper to another player, type ```:whisper <player username> <message>``` or ```:w <player username> <message>``` for short.

[![asciicast](https://asciinema.org/a/95044.png)](https://asciinema.org/a/95044)

### Fog of War
To toggle FoW from the main command window press ```f```. To edit the FoW press ```F``` to enter the FoW editing menu. ```a``` will add fog to a space, ```r``` will remove fog from a space. As with all commands, they can be used with motions: e.g. ````20 a l``` to add 20 blocks of fog to the right of the initial cursor position.

[![asciicast](https://asciinema.org/a/95045.png)](https://asciinema.org/a/95045)

### Rolling Dice
To roll dice type ```:roll <number of rolls>d<number of sides on die>``` or ```:r <number of rolls>d<number of sides on die>```. Use ```ctrl+j``` to scroll down and ```ctrl+k``` to scroll the results up and down.

[![asciicast](https://asciinema.org/a/95046.png)](https://asciinema.org/a/95046)
