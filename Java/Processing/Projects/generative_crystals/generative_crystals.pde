int CRYSTAL_SIZE = 500;
int CRYSTAL_SIDES = 6;
color[] PALLETTE;

void setup()
{
  size(2000, 1000);
  colorMode(HSB, 360, 100, 100);
  
  PALLETTE = new color[2];
  PALLETTE[0] = color(182, 100, 100);
  PALLETTE[1] = color(310, 100, 100);
}

void draw()
{
  test_lines();
}

void test_lines()
{
  push();
    noFill();
    strokeWeight(3);

    stroke(PALLETTE[0]);
    translate(width/2, height/2);
    circle(0, 0, CRYSTAL_SIZE);
    
    stroke(PALLETTE[1]);
    float angle = radians(360 / CRYSTAL_SIDES);
    // Drawing the lines
    for (int i = 0; i < CRYSTAL_SIDES; i++)
    {
      line(0, 0, 0, CRYSTAL_SIZE / 2);
      rotate(angle);  
    }
  pop();
}
