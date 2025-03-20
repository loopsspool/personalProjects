// Ethan Jones 
// 10:35pm, Wednesday 12-19-18 

// stars.js
// Stars that move on the screen

/* TODO: Create moving patterns
         Selector for patterns
         Make stars reset only when moving offscreen and move to onscreen (instead of big wheel)
            - Intended for optomization and potetially cool affects that look different
        
*/

var WW;
var WH;
var stars = [];
var movementSelector; // Set to be html drop down list?

function setup()
{
    WW = windowWidth;
    WH = windowHeight;
    noStroke();
    ellipseMode(CENTER);

    initializeStars();
}

function draw()
{       
    background(238, 100, 16);
    runArrays();    
    rotationAcc += 2;
}

function runArrays()
{
    for (var i=0; i<stars.length; i++)
        stars[i].display();
}

function initializeStars()
{
    for (let i=0; i<2000; i++)
        stars.push(new star(random(-1.2*WW,1.2*WW), random(-1.2*WW,1.2*WW), random(70,100)));
};

function star(x, y, initBrightness)
{
    this.x = x;
    this.y = y;
    this.size = random(1,4);
    this.brightness = initBrightness;
  
    this.display = function()
    {
        fill(50, 90, this.brightness);
        ellipse(this.x, this.y, this.size, this.size);
        this.twinkle();
    }

    // TODO: Make movements based off of movement selector value
    this.move = function
    {
        // TODO: Add conditional to see if star is offscreen, if so call this.reset()
        push();
        rotate(rotationAcc/12);
        pop();
    }
    
    // TODO: Make twinkle perlin noise based?
    this.twinkle = function()
    {
        this.brightness = random(30,70);
    }

    this.reset = function()
    {
        // TODO: make it so stars new x, y value is random on screen
    }
};

function windowResized()
{
    WW = windowWidth;
    WH = windowHeight;
    resizeCanvas(WW, WH);
}
