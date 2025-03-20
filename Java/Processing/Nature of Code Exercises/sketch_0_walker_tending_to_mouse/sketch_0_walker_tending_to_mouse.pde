walker w;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  frameRate(120);
  
  w = new walker();
  
  background(360);
}

void draw()
{
  w.step();
  w.display();
}
