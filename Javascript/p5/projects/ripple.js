// ripple.js
// Creates some nice ripples

// Ethan Jones 
// 3-5-2019 4:24pm

var WW, WH;
var centerCircleSize = 30;
ripple = 
{
    x;
    y;
    strokeWidth;
    // Use arcs
}

function setup()
{
    WW = windowWidth;
    WH = windowHeight;
    createCanvas(WW, WH);
    colorMode(HSB, 360, 100, 100, 100);
    angleMode(DEGREES);
    noFill();
}

function draw()
{
    background(184, 30, 100);
    ellipse(WW/2, WH/2, centerCircleSize, centerCircleSize);

}



function windowResized()
{
    WW = windowWidth;
    WH = windowHeight;
    resizeCanvas(WW, WH);
}