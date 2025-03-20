mover m;

void setup()
{
  size(2160, 1024);
  colorMode(HSB, 360, 100, 100);
  
  m = new mover();
}

void draw()
{
  m.update();
  m.check_edges();
  m.display();
}
