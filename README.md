# SVGtarien
Revolutionnary progamming language and compiler to generate SVG files

## Examples

### Simple description

Input :
```
title("Exemple simple de figure SVG")
desc("Cette figure est constituée d'un rectangle, d'un segment de droite et d'un cercle.")

pos(0, 70)             # set the pointer at x=0, y=70
fill(green)            # set the fill color state to green
move(100, 80)          # move the pointer to 100,80
rect()                 # draw a rectangle width (x1,y1) = the penultimate position and (x2,y2) = the last position
pos(5, 5)
move(245, 90)
noFill()               # reset the fill color state
stroke(red)            # set the stroke color to red
line()	
pos(90, 80)
width(4)               # set the stoke-width attribute to 4 pixels
ellipse(50)
pos(180, 60)
text("Un texte")
```

Output :
```xml
<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="300" height="200">
  <title>Exemple simple de figure SVG</title>
  <desc>
    Cette figure est constituée d'un rectangle,
    d'un segment de droite et d'un cercle.
  </desc>
 
  <rect width="100" height="80" x="0" y="70" fill="green" />
  <line x1="5" y1="5" x2="250" y2="95" stroke="red" />
  <circle cx="90" cy="80" r="50" stroke="red" stroke-width="4"/>
  <text x="180" y="60">Un texte</text>
</svg>
```

### Drawing

#### Setting state attributes

Positions
```
pos(200,300) # set the pointer to x=200, y=300 -------------- x=200, y=300
posx(150)    # set only the x coordinate, the new position is x=150, y=300
posy(250)    #                            the new position is x=150, y=250
move(5,10)   # move the pointer           the new position is x=155, y=260
movex(-55)   # move only in x             the new position is x=100, y=260
movey(30)    #                            the new position is x=100, y=290

# get the current postition
$actualPos = pos()
$x = posx()
$y = posy()
```

Color and width
```
fill("red")               # set the fill color of next elements to red
stroke("#ffff00")         # set the stroke color of next elements to yellow
width(5)                  # set the stroke width
rect()                    # draw a red rectangle with a 5px yellow stroke
noFill()                  # reset the fill color attribute
rect()                    # draw a transparent rectangle with a 5px yellow stroke 
noStroke()                # reset the stroke color attribute
fill("rgba(0,0,255,0.5)") # set the fill color to semi-transparent-blue
rect()                    # draw a semi-transparent-blue rectangle with no stroke

# get the current fill color
$currentColor = fill()
```

Shapes are drawn using the currents attrbutes of the program.
The position and size of the shape you draw is defined by the last positions you set.
Before calling a shape function, like `rect` or `line`, you need to move the position pointer 2 times.

#### Rectangles

Draw a sqare 150px wide starting in x=50, y=100  
```
pos(50,100)
pos(200,250)
rect()
```
Same thing using relative position
```
pos(50,100)
move(150,150)
rect()
```

#### Lines

Draw à line passing through 3 points
```
pos(200,300)
pos(100,350)
pos(150,350)
line()
```
Same thing using relative position
```
pos(200,300)
move(-100,50)
movex(50)
line()
```

#### Circles and ellipses

Draw a 5px radius circle in x=30, y=60
```
pos(30,60)
ellipse(5)
```
Draw an ellipse
```
pos(30,60)
ellipse(5,12)
```

### Loops

Draws 10 circles of radius 40 spaced with 100 pixels
```
pos(0, 200)
$x = 0
while ($x < 10){
	posx($x * 100)
	ellipse(40)
}
```

### Functions
 
```
function drawCircle($x, $y, $r){
	pos($x, $y)
	ellipse($r)
}
```
