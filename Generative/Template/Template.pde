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
}

void draw()
{
  
}
