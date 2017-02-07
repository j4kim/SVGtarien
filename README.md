# SVGtarien
Revolutionnary progamming language and compiler to generate SVG files

## Examples

### Simple example

Input :
```
title("Exemple simple de figure SVG")
desc("Cette figure est constituée d'un rectangle, d'un segment de droite et d'un cercle.")

pos(0, 70)           # set the pointer at x=0, y=70
fill("green")        # set the fill color state to green
move(100, 80)        # move the pointer to 100,80
rect()               # draw a rectangle from the penultimate position to the last position
pos(5, 5)
move(245, 90)
nofill()             # reset the fill color state
stroke("red")        # set the stroke color to red
line(2)	             # draw a line linking the two last positions set
pos(90, 80)
width(4)             # set the stoke-width attribute to 4 pixels
ellipse(50)          # draw a 5-radius circle
pos(180, 60)
text("Un texte")
```

Output code :
```xml
<?xml version="1.0" encoding="utf-8"?>
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="250.0" height="150.0">
    <title>Exemple simple de figure SVG</title>
    <desc>
         Cette figure est constituée d'un rectangle,
	 d'un segment de droite et d'un cercle.
    </desc>
    <rect x="0.0" y="70.0" width="100.0" height="80.0" fill="green" />
    <polyline points="250.0,95.0 5.0,5.0 " stroke="red" />
    <ellipse cx="90.0" cy="80.0" rx="50.0" ry="50.0" stroke-width="4.0" stroke="red" />
    <text x="180.0" y="60.0" >Un texte</text>
</svg>
```

Output image :  
![Simple example](http://svgshare.com/i/ek.svg)

### Drawing

#### Setting state attributes

Input :
```
pos(100,50)               # set postion cursor at x=100 and y=50
fill("red")               # set the fill color of next elements to red
stroke("#ffff00")         # set the stroke color of next elements to yellow using hexadecimal notation
width(5)                  # set the stroke width
rect(75)                  # draw a 75px red square with a 5px yellow stroke

nostroke()                # reset the stroke attributes (color and width)
fill(0, 0, 255, 0.5)      # set the fill color to semi-transparent-blue using rgba notation
move(200, 0)              # move the postition cursor by 200px to the right, new position is 300,50
move(50,200)              # new position is 350,250
rect()                    # draw a semi-transparent-blue rectangle with no stroke
```

Output :  

![Attributes example](http://svgshare.com/i/fq.svg)

Shapes are drawn using the currents attributes of the program (state).
The position and size of the shape you draw is defined by the last positions you set.
Before calling a shape function, like `rect` or `line`, you need to set or move the position pointer 2 times.

The size of the drawing is automatically detect, you can also use the `size(w,h)` method.

#### Rectangles

Draw a square 150px wide starting in x=50, y=100  
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
Same thing using a parameter passed in `rect` method
```
pos(50,100)
rect(150)
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

By default `line` draws a polyline passing through all postitions in history. You can set a parameter to the `line` method that defines the number of points used to draw the line. You can also use the `clean` method to reset the position history.

Input :
```
fill("none")
pos(0,0)
move(50,20)
move(30,60)
line()

move(200,-30)
stroke("red")
line(2)

clean()
pos(300,100)
move(-100,50)
stroke("blue")
line()
```

Output :  

![lines](http://svgshare.com/i/gH.svg)

#### Circles and ellipses

Draw a 5px radius circle centered in x=30,y=60
```
pos(30,60)
ellipse(5)
```
Draw an ellipse centered in x=30,y=60, with x-radius=5 and y-radius=12
```
pos(30,60)
ellipse(5,12)
```

#### Bézier curves

#### Text

#### Advanced attributes

rotate
scale
notransform

### Programming elements

#### if else statements

#### Loops

Draws 10 circles of radius 40, spaced by 100 pixels
```
pos(0, 200)
$x = 0
while ($x < 10){
	posx($x * 100)
	ellipse(40)
}
```

#### Built-in functions

sin cos tan s i rand

#### Routines
 
```
function drawCircle($x, $y, $r){
	pos($x, $y)
	ellipse($r)
}
```
