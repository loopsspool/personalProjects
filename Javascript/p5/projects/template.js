// template.js
// Template for p5 files

// Ethan Jones 
// 3-5-2019 4:24pm

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
    
}

function windowResized()
{
    WW = windowWidth;
    WH = windowHeight;
    resizeCanvas(WW, WH);
}