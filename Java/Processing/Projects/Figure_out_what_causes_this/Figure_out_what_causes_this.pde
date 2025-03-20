int amount_of_rings;
Ring[] rings;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100, 100);
  strokeWeight(10);
  noFill();
  background(0);
  
  amount_of_rings = 10;
  rings = new Ring[amount_of_rings];
  for (int i = 0; i < amount_of_rings; i++)
    rings[i] = new Ring(width, height, 0, width/2, i * height/amount_of_rings, 200, 50, -QUARTER_PI, PI + QUARTER_PI, 360);
}

void draw()
{
  noStroke();
  fill(0, 5);
  rect(0, 0, width, height);
  
  for (int i = 0; i < amount_of_rings; i++)
  {
    rings[i].move();
    rings[i].display();
  }
}
