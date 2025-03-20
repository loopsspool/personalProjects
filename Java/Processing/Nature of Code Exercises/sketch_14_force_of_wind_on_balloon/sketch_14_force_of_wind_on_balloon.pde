Balloon b;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  
  b = new Balloon();
}

void draw()
{
  background(280);
  b.update();
  b.display();
}
