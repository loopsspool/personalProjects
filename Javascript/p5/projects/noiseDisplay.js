// noiseDisplay.js
// Visualizes perlin noise in different ways all at once

// Ethan Jones
// 8:29pm, Thursday 12-20-18

var WW;
var WH;
var noiseScale = 0.02;
var windowDivision = 2;

function setup()
{
    WW = windowWidth;
    WH = windowHeight;
    createCanvas(WW, WH);
}

function draw()
{
    background(0);
    wavyMouseNoise();
}

function wavyMouseNoise()
{
    // TODO: Constrain lines to windowDivision
    for (var x=0; x < WW/windowDivision; x++)
    {
        var noiseVal = noise((mouseX+x)*noiseScale, mouseY*noiseScale);
        stroke(noiseVal*255);
        line(x, mouseY+noiseVal*80, x, WH/windowDivision);
    }
}

function windowResized()
{
    WW = windowWidth;
    WH = windowHeight;
    resizeCanvas(WW, WH);
}
