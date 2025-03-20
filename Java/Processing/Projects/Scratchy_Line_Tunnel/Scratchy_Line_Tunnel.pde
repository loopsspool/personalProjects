int rand_x, rand_y;
int last_x, last_y;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100, 100);
  frameRate(3000);
  
  rand_x = width/2;
  last_x = width/2;
  rand_y = height/2;
  last_y = height/2;
}

void draw()
{
  line(last_x, last_y, rand_x, rand_y);
  reset_points();
}

void reset_points()
{
  last_x = rand_x;
  last_y = rand_y;
  rand_x = floor(random(width));
  rand_y = floor(random(height));
}
