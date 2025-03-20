// clouds.js
// Creates the illusion of clouds

var WW, WH;

function setup()
{
    WW = windowWidth;
    WH = windowHeight;
    createCanvas(WW, WH);
    colorMode(HSB, 360, 100, 100, 100);
}

function draw()
{
    fill(0);
    ellipse(WW/2, WH/2, 20, 20);
}

function windowResized()
{
    WW = windowWidth;
    WH = windowHeight;
    resizeCanvas(WW, WH);
}