// raindrops.js
// raindrops

// Ethan Jones 
// 5-18-2019 10:06pm

var WW, WH;
var radius, size_inc, max_size, min_size;
var ellipse_amount;
var coordX = [], coordY = [];

// TODO: Make each raindrop have a lifespan so when it's finished expanding a new one comes on
// TODO: Transparents waves from drop
// TODO: Assess to make drops individual objects?
function setup()
{
    WW = windowWidth;
    WH = windowHeight;
    createCanvas(WW, WH);
    colorMode(HSB, 360, 100, 100, 100);
    stroke(0);
    strokeWeight(3);

    min_size = 2;
    radius = min_size;
    size_inc = 4;
    max_size = 100;

    ellipse_amount = 20;
    for (var i = 0; i < ellipse_amount; i++)
    {
        // TODO: Use perlin noise instead?
        coordX[i] = random(WW);
        coordY[i] = random(WH);
    }
}

function draw()
{
    background(100);

    for (var i = 0; i < ellipse_amount; i++)
    {
        // TODO: Use perlin noise instead?S
        ellipse(coordX[i], coordY[i], radius, radius);
    }
    //ellipse(WW/2, WH/2, radius, radius);

    update_size();
}

function update_size()
{
    radius += size_inc;    

    if (radius >= max_size)
        radius = min_size;
}

function windowResized()
{
    WW = windowWidth;
    WH = windowHeight;
    resizeCanvas(WW, WH);
}