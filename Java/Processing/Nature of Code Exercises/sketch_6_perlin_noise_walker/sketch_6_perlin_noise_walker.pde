walker w;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 0, 0);
  
  w = new walker();
}

void draw()
{
  w.display();
  w.step();
}
