//pixelizer.js
//Ethan Jones   12/17/2018
// 5 hrs (3 just into resizing images larger than canvas from DOM)

//Takes an image via file browse from the user and pixelates said image

var WW, WH; //window width & height
var pic;
var input;
var img;
var first;
var pixelSize = 0.4;
var col;
var shouldDec = false;
var shouldInc = true;
var pixelVariator = 0.005;
var x, y, d; // set these to the coordinates 
var off = (y width + x) d * 4; var components = [ pixels[off], pixels[off + 1], pixels[off + 2], pixels[off + 3] ]; print(components);

function setup()
{
    WW = windowWidth;
    WH = windowHeight;
    createCanvas(WW, WH);
    colorMode(HSB, 360, 100 , 100, 100);
    rectMode(CENTER);
    noStroke();
    input = createFileInput(handleFile);
    input.position(0, 0); 
} 

function draw() 
{
    //TODO: no loop until interaction detected with file input
    //noLoop();
    if(img)
    {
        resizeImg(img);
        pixelater();
        image(img,0,0);
    }
} 

function handleFile(file) 
{ 
    if (file.type === 'image') 
    {
        img = loadImage(file.data);
        img.loadPixels();
        first = true;
    }
}

function resizeImg(im)
{
    if(im.width > WW)
        im.resize(WW, 0);    
    else if(im.height > WH)
        im.resize(0, WH);    
}

function pixelater()
{
    //Works okay but can't see enlarging pixels how I wanted... See commented code for reference
    //Looks like it isn't grabbing color correctly and also takes TOO DAMN LONG. Look at get() reference in p5 reference to see pixel array optomization
    // console.log(img.height, img.width);
    // for (let h = 0; h < img.height; h += pixelSize)
    // {
    //     for (let w = 0; w < img.width; w += pixelSize)
    //     {
    //         console.log(w, h);
    //         col = get(w, h);
    //         console.log(col);
    //         fill(col);
    //         rect(w, h, pixelSize, pixelSize);
    //     }
    // }
    if (frameCount % 5 == 0)
    {
        if (pixelSize >= 0.4)
        {
            shouldDec = true;
            shouldInc = false;
        }
        if (pixelSize <= 0.1)
        {
            shouldInc = true;
            shouldDec = false;
        }
        if (shouldInc)
            pixelSize += pixelVariator;
        if (shouldDec)
            pixelSize -= pixelVariator;
        pixelDensity(pixelSize);
        console.log(pixelSize);
    }
}

function windowResized()
{
    WW = windowWidth;
    WH = windowHeight;
    resizeCanvas(WW, WH);
}
