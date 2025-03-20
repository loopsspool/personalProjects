Ball[] balls;
int amount_of_balls = 70;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  noStroke();
  
  balls = new Ball[amount_of_balls];
  for (int i = 0; i < amount_of_balls; i++)
    balls[i] = new Ball(10);
}

void draw()
{
  for (int i = 0; i < amount_of_balls; i++)
  {
    balls[i].update();
    balls[i].display();
  }
}
