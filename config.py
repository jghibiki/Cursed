from parser import add_color, add_color_pair, add_feature


##########
# Colors #
##########
#
# Note: "White" and "Black" are defined by default
#

add_color("Light Red",      255,    118,    118)
add_color("Red",            255,    0,      0)
add_color("Dark Red",       133,    0,      0)

add_color("Light Green",    118,    255,    118)
add_color("Green",          0,      255,    0)
add_color("Dark Green",     0,      133,    0)

add_color("Light Blue",     118,    118,    255)
add_color("Blue",           0,      0,      255)
add_color("Dark Blue",      0,      0,      133)

add_color("Light Grey",     200,    200,    200)
add_color("Grey",           138,    138,    138)
add_color("Dark Grey",      94,     94,     94)

add_color("Brown",          145,    73,     0)

add_color("Gold",           255,    200,    0)

add_color("Orange",         255,    150,    0)


###############
# Color Pairs #
###############
# Color Pairs are a pairing of a foreground and a background color.
#
# Note: Color pairs consisting of any color and a black background are defined automatically and are named after the foreground color
#

add_color_pair("Blue on Light Blue",    "Blue",     "Light Blue")
add_color_pair("Red on Orange",         "Red",      "Orange")



#################
# Feature Types #
#################

add_feature("Wall",                      "▒",    "Brown")
add_feature("Table",                     "T",    "Brown")
add_feature("Chair",                     "c",    "Brown")
add_feature("Door",                      "d",    "Brown")
add_feature("Up Stair",                  "↑",    "White")
add_feature("Down Stair",                "↓",    "White")
add_feature("Lantern",                   "%",    "Gold")
add_feature("Road",                      "▒",    "Grey")
add_feature("Chest",                     "#",    "White")
add_feature("Point of Interest",         "#",    "White")
add_feature("Gate",                      "G",    "Brown")
add_feature("Water",                     "~",    "Light Blue")
add_feature("Tree",                      "O",    "Green")
add_feature("Bush",                      "o",    "Light Green")
add_feature("Grass",                     ".",    "Light Green")
add_feature("Hill",                      "^",    "White")
add_feature("Bed",                       "b",    "Brown")
add_feature("Statue",                    "&",    "White")
add_feature("Blood",                     "▒",    "Dark Red")
add_feature("Fire",                      "~",    "Red on Orange")
add_feature("Snow",                      "▒",    "White")
add_feature("Boulder",                   "O",    "Dark Grey")
