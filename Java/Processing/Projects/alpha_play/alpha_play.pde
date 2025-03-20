float alpha;
Ball ball;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100, 100);
  noStroke();
  
  // background so alpha workaround doesn't fade in
  fill(186, 99, 64);
  rect(0, 0, width, height);
  
  alpha = 10;
  
  ball = new Ball(90, 90, 80, 160, 10, 5);
}

void draw()
{  
  // Workaround for alpha channel not working with background
  fill(186, 99, 64, alpha);
  rect(0, 0, width, height);

  ball.display();
  ball.move();
}
