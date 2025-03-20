mover m;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  
  m = new mover();
}

void draw()
{
  m.update();
  m.display();
  
}
