float t = 0;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  
  frameRate(200);
}

void draw()
{
  float n = noise(t);
  // CHANGE THIS INCREMENTER VALUE TO SEE DIFFERENCE IN VALUE CHOPPINESS
  t += 0.001;
  
  float x = map(t, 0, 20, 0, 800);
  float y = map(n, 0, 1, 800, 0);
  
  fill(0);
  circle(x, y, 3);
}
