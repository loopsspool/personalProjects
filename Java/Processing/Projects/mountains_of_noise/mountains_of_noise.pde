mountain[] mountains;

void setup()
{
  size(2400, 1200);
  colorMode(HSB, 360, 100, 100);
  background(270, 100, 16);
  
  int amount_of_mountains = 4;
  mountains = new mountain[amount_of_mountains];
  
  // STARS
  for (int i = 0; i < 200; i++)
  {
    fill(48, 30, 100);
    circle(random(width), random(height/6), 3);
  }
  
  // MOUNTAINS
  for (int i = 0; i < amount_of_mountains; i++)
  {
    float mountain_y_start = map(i, 0, amount_of_mountains, 150, 7 * height/8);
    mountains[i] = new mountain(mountain_y_start);
    mountains[i].build_mountain();
    noStroke();
    fill(214, map(i, 0, amount_of_mountains, 60, 100), 70);
    mountains[i].display();
  }
}

void draw()
{

}
