// pixel_drip_on_click.js
// USer can choose image
    // When clicked and held, clicked pixel "drips"

// Ethan Jones 
// 6-5-2019 2:39pm

var WW, WH;
let img;
let drip_size = 10;
let drip_acc = 0;
let pixel_x, pixel_y, pixel, pixel_h, pixel_s, pixel_b;

function setup()
{
    WW = windowWidth;
    WH = windowHeight;
    createCanvas(WW, WH);
    noStroke();
    // Unfortunately must use RGB since that is what is used in get()
        // Unless include an RGB > HSB color conversion function
    //colorMode(HSB, 360, 100, 100, 100);
    
    img = loadImage('../../../../pacific beach.jpg');
    
}


function draw()
{
    image(img, 0, 0);
    //updatePixels();
    // TODO: Put into where it isn't being constantly called
    img.resize(WW, WH);
    
    if (mouseIsPressed)
    {
        drip_acc++;
        //set(pixel_x, pixel_y + drip_acc, pixel);
        // TODO: If you want this to actually update the image, use set in a for loop going -drip_size/2 to drip_size/2 around current pixel
        rect(pixel_x, pixel_y, drip_size, drip_acc);
    }
    else
        drip_acc = 0;
}


function mousePressed()
{
    pixel_x = mouseX;
    pixel_y = mouseY;
    pixel = get(pixel_x, pixel_y);
    pixel_h = hue(pixel);
    pixel_s = saturation(pixel);
    pixel_b = brightness(pixel);
    fill(pixel);
}


function windowResized()
{
    WW = windowWidth;
    WH = windowHeight;
    resizeCanvas(WW, WH);
}