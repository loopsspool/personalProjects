float x;
float y;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  
  x = width/2;
  y = height/2;
}

void draw()
{
  float sd = 2;
  x += 2 * randomGaussian();
  y += 2 * randomGaussian();
  
  fill(0);
  circle(x, y, 5);
}
