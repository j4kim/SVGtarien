# SVGtarien
Revolutionnary progamming language and compiler to generate SVG files

## Examples

### Simple description

Input :
```
title "Exemple simple de figure SVG"
desc "Cette figure est constituée d'un rectangle, d'un segment de droite et d'un cercle."
pos 0 70
fill green
move 100 80
rect
pos 5 5
move 245 90
stroke red
line	
pos 90 80
fill blue
circle 50
pos 180 60
text "Un texte"
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
  <circle cx="90" cy="80" r="50" fill="blue" />
  <text x="180" y="60">Un texte</text>
</svg>
```

### loops

```
pos 0 200
$x = 0
while ($x < 10){
	posx $x * 100
	circle
}
```

### functions

```
function drawCircle($a, $b, $r){
pos $a $b
circle $r
}
```
