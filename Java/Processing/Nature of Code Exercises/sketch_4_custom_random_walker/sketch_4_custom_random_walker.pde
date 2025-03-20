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
  float step_size = monteCarlo();
  x += random(-step_size, step_size);
  y += random(-step_size, step_size);
  
  fill(0);
  circle(x, y, 16);
}

float monteCarlo()
{
  while (true)
  {
    float r1 = random(10);
    float probability = r1;
    float r2 = random(10);
    
    if (r2 < probability)
      return r1;
  }
}
