int amount_of_steps;
color bg_color;
Step[] steps;

void setup()
{
  size(1000, 800);
  colorMode(HSB, 360, 100, 100, 100);
  strokeWeight(25);
  noFill();
  bg_color = color(288, 98, 25);
  background(bg_color);
  
  amount_of_steps = 4;
  steps = new Step[amount_of_steps];
  for (int i = 0; i < amount_of_steps; i++)
    steps[i] = new Step(width, height, 0, width/3, i * height/amount_of_steps, 2*width/3, 2, 4, color(174, 91, 99));
}

void draw()
{
  noStroke();
  // Transparent background workaround
  fill(bg_color, 5);
  rect(0, 0, width, height);
  
  for (int i = 0; i < amount_of_steps; i++)
  {
    steps[i].move();
    steps[i].display();
  }
}
