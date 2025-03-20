int AMOUNT_OF_CIRCLES;
color bg = #FFECD3;

void settings()
{
  // Setting ssketch window to left side of screen
  // -70 accounts for navigation bar
  size(int(displayWidth/2), int(displayHeight - 70));
}

void setup()
{
  surface.setLocation(0, 0);
  frameRate(1);
  
  colorMode(HSB, 360, 100, 100, 100);
  noStroke();
  background(bg);
  AMOUNT_OF_CIRCLES = int(random(10));
}

void draw()
{
  background(bg);
  for (int i=0; i<AMOUNT_OF_CIRCLES; i++)
  {
    if (random(1) < 0.2)
      fill(bg);
    else
      fill(int(random(360)), random(20, 80), random(20, 70));
    circle(random(width), random(height), random(width/7, width/2));
  }
}
