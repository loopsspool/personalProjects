int frame;
int rings;
int rand;
PGraphics copy;

void setup()
{
  size(850, 850);
  colorMode(HSB, 360, 100, 100, 100);
  frameRate(15);
  strokeWeight(1);
  //noFill();
  stroke(360);
  fill(320, 30);
  background(200);
  
  // This will copy the final image the ellipses create
  copy = createGraphics(width, height);
  
  rings = 30;
  rand = 1;
}

void draw()
{
  push();
  translate(width/2, height/2);
  frame = frameCount%rings;
  rotate (QUARTER_PI * radians(frame * rand));
  // Before bakground otherwise largest ring will always show
  ellipse (0, 0, 10 * frame, 30 * frame);
  copy.beginDraw();
  copy.ellipse (0, 0, 10 * frame, 30 * frame);
  copy.endDraw();
  
  if (frame == rings - 1)
  {
    //delay(1500);

    /* TODO:
     * Instead of just delay, save as image
     * Then enlarge a lil over time
     * Then fade out while next ellipse sequence is about to begin
    */
    for (int i = 0; i < 60; i++)
    {
      // Now ideally this is supposed to do the above
      // ... It doesn't.
      // But it still provides a delay effect, which is nice
        // to have time to view the visuals
      // TODO: Fix the below somehow
      scale(2);
      image(copy, 0, 0);
    }
    //delay(1500);
    background(200);
    rand = floor(random(1, 90));
  }
  pop();
}
