// autoDrawing.js
// Computer draws stuff

// TODO: Make single object oriented?

var WW, WH;
var shapes = [];
var chosenShape, chosencolor, chosenSize, maxSize;
var x = [];
var y = [];

function setup()
{
    // ENVIORNMENT INITIALIZERS
    WW = windowWidth;
    WH = windowHeight;
    createCanvas(WW, WH);
    colorMode(HSB, 360, 100, 100, 100);
    noStroke();

    //VARIABLE INITIALIZERS
    shapes.push('circle');
    shapes.push('square');
    shapes.push('triangle');
    shapes.push('line');

    x = [0, 0, 0, 0];
    y = [0, 0, 0, 0];

    chosencolor = {h:0, s:0, l:0, a:0};

    maxSize = 100;
}

function draw()
{
    selectProperties();
    drawShape();
}

function selectProperties()
{
    // Chooses shape
    chosenShape = shapes[Math.floor(Math.random() * shapes.length)];
    // Randomizes coordinates
    for (let i = 0; i < x.length; i++)
    {
        x[i] = random(0, WW);
        y[i] = random(0, WH);
    }
    // Chooses coloer
    chosencolor.h = random(360);
    chosencolor.s = random(100);
    chosencolor.l = random(100);
    chosencolor.a = random(100);
    // Chooses size
    chosenSize = random(maxSize);
}

// TODO: fill in all parameters
function drawShape()
{
    fill(chosencolor.h, chosencolor.s, chosencolor.l, chosencolor.a);

    if (chosenShape == 'circle')
        ellipse(x[0], y[0], chosenSize, chosenSize);
    if (chosenShape == 'square')
        rect(x[0], y[0], chosenSize, chosenSize);
    if (chosenShape == 'triangle')
        triangle(x[0], y[0], x[1], y[1], x[2], y[2]);
    if (chosenShape == 'line')
        line(x[0], y[0], x[1], y[1]);
}

function windowResized()
{
    WW = windowWidth;
    WH = windowHeight;
    resizeCanvas(WW, WH);
}