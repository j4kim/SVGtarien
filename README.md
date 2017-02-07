# SVGtarien
Revolutionnary progamming language and compiler for [SVG](https://en.wikipedia.org/wiki/Scalable_Vector_Graphics) images generation.  
The compiler is made in Python 3 and uses [ply](http://www.dabeaz.com/ply/ply.html) (Python [Lex](https://en.wikipedia.org/wiki/Lex_(software)) and [Yacc](https://en.wikipedia.org/wiki/Yacc)).

Our language is based on states. Most of the drawing attributes are set globally using specific methods.  
That means, for example, to draw two circles with the same attributes, you won't write :
```
circle(x=20, y=30, radius=10, stroke-width=2, stroke-color='black', fill="red")
circle(x=80, y=30, radius=10, stroke-width=2, stroke-color='black', fill="red")

# only the x position has changed, but the lines are mostly repetitive -> bad
```

But you will write :
```
pos(20,30)
width(2)
stroke("black")
fill("red")
ellipse(10) # draw a circle with previously set attributes
move(60,0)  # change the position state
ellipse(20) # draw a circle with previously set attributes, but at the new position

# more lines, but no repetitons -> good
```

By doing so, we aim to simplify SVG images generation avoiding its verbosity.  

The language provides a few methods for writing elements in the SVG file and for changing the attributes of those elements.  
* Drawing methods
    * `rect`, `line`, `ellipse`, `text`, `bezier`
* Attributes modification methods :
    * `fill`, `nofill`, `stroke`, `nostroke`, `width`, `font`, `rotate`, `scale`, `notransform`
* Position state methods :
    * `pos`, `move`, `clean`
* Special methods :
    * `size`, `title`, `desc`

See examples below to learn more about the language.

# Examples

## Simple example

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

## Drawing

### Setting state attributes

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

### Rectangles

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

### Lines

By default, the `line` method draws a polyline passing through all postitions in history. You can set a parameter to the `line` method that defines the number of points used to draw the line. You can also use the `clean` method to reset the position history.

Input :
```
fill("none")      # by default, polylines are filled, you must set this if you juste want lines
stroke("black")   # you must also define a stroke color
width(8)          # set the stroke-width attribute

pos(0,0)          # history : [(0,0)]
move(50,20)       # history : [(0,0),(50,20)] 
move(30,60)       # history : [(0,0),(50,20),(80,80)]
line()            # draw a line passing through the 3 points in history

width(4)
move(100,-30)    # history : [(0,0),(50,20),(80,80),(180,50)]
stroke("red")
line(3)          # draw a red line using the 3 last positions in history

clean()          # history : []
pos(300,100)     # history : [(300,100)]
move(-100,50)    # history : [(300,100),(200,150)]
move(0,20)       # history : [(300,100),(200,150),(300,170)]
stroke("blue")
line()           # draw a line passing through the 3 points in history
```

Output :  

![lines](http://svgshare.com/i/en.svg)

### Circles and ellipses

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

### Bézier curves

The `bezier` method allows you to draw [quardatic bezier curves](https://upload.wikimedia.org/wikipedia/commons/3/3d/B%C3%A9zier_2_big.gif) using the 3 last points in history.

Input :
```
size(300,150)   # fix the image size

fill("red")

pos(50,30)
ellipse(10)     # first control point at (50,30)
move(50,100)
ellipse(10)     # second control point at (100,130)
move(180,-80)
ellipse(10)     # third control point at (280,50)

fill("none")    # I don't want to fill my bezier curve
stroke("black") # it wont appear if it has no stroke
width(5)

bezier()        # draw a bezier curve using the 3 control points
```

Output :  

![Bezier](http://svgshare.com/i/gp.svg)

You can add a parameter to the `bezier` method if you want the curve to be closed : `bezier(1)` :

![Closed bezier](http://svgshare.com/i/g8.svg)

### Text

You can custom texts using the `font` method : 
```
size(870,150)

pos(20,20)
text("SVGtarien")

move(150,30)
font(32)
text("is really")

move(150,30)
font(32, "Sans-serif")
text("amazing")

move(150,30)
font(32, "cursive")
text("powerful")

move(150,30)
font(32, "fantasy")
text("revolutionnary !")
``` 

Output :

![fonts](http://svgshare.com/i/f5.svg)

### Advanced attributes

rotate
scale
notransform

## Programming elements

### Variables

Variables are prefixed with `$`. You can define a variable like this : `$x = 12`

### if else statements

### Loops

Draws 10 circles of radius 20, spaced by 80 pixels
```
size(870,150)

pos(0, 75)

$i = 0
while ($i < 10){
    move(80,0)
    ellipse(20)
    $i = $i + 1
}
```

Output :

![10 cercles](http://svgshare.com/i/gJ.svg)

### Built-in functions

There is a few built-in functions you may need to use :
* Trigonometric functions : `sin`, `cos`, `tan` takes a radian angle as parameter
* Casting : `s` for string and `i` for integer (by default, all numbers are float)
* Pseudo-random generator : `rand` accept 0, 1 or 2 parameters
    * `rand()` returns a floating points number between 0 and 1 (excluded)
    * `rand(12)` returns a integer between 0 and 11
    * `rand(-12, 12)` returns a integer between -12 and 11
* Debugging : the `debug` function may help, it just prints the arguments given values in the console.

Example using `sin` :
```
$w = 870
$h = 150
size($w,$h)

$PI = 3.14159265359
$x = 0
while($x <= $w){
    $y = $h/2 - sin($PI*4*$x/$w) * $h/2
    pos($x,$y)
    $x = $x + 10
}
stroke("black")
fill("none")
line()
```

Output :

![sinus](http://svgshare.com/i/gq.svg)

Example using `rand` and `i` :
```
$w = 870
$h = 150
size($w,$h)

$x = 0
while($x <= $w){
    $y = rand($h)                      # choose a random vertical position
    pos($x,$y)

    $red = 255*$x/$w                   # set the red component relative to horizontal position
    $green = 255 - $red                # the green component is the inverse
    $blue = 255*$y/$h                  # set the blue component relative to vertical position
    $alpha = rand()                    # the opacity is totally random
    fill($red, $green, $blue, $alpha)

    ellipse(i(25 - $alpha * 25))       # draw a circle with radius inversely proportional to its opacity
    $x = $x + 1                        # iterate through each horizontal pixel
}
```

Output :

![random circles](http://svgshare.com/i/g7.svg)

### Routines
 
```
function drawCircle($x, $y, $r){
	pos($x, $y)
	ellipse($r)
}
```
