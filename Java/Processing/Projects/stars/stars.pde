int amount_of_starting_stars, max_stars;
int current_stars;
Star s;
Star[] stars;

void setup()
{
  size(1000, 1000);
  
  colorMode(HSB, 360, 100, 100);
  noStroke();
  
  amount_of_starting_stars = 4;
  current_stars = amount_of_starting_stars;
  max_stars = 100;
  
  stars = new Star[max_stars];
  for (int i = 0; i < amount_of_starting_stars; i++)
  {
    stars[i] = new Star();
  }
}

void draw()
{
  background(240, 99, 35);
  
  if ((frameCount%20 == 0) && (current_stars < max_stars))
  {
    stars[current_stars] = new Star();
    current_stars++;
  }
  
  // All get bright and dim together for some reason?
  for(int i = 0; i < current_stars; i++)
  {
    stars[i].display();
    stars[i].alter_brightness(int(random(20,101)));
  }
}
