PImage rachel;
Ollie[] ollies;
int amount_of_ollies = 30;

void setup()
{
  size(600, 1000);
  surface.setResizable(true);
  surface.setLocation(500, 0);
  colorMode(HSB, 360, 100, 100);
  
  rachel = loadImage("rachel cubed.jpg");
  rachel.resize(width, height);
  //image(rachel, 0, 0, width, height);
  
  ollies = new Ollie[amount_of_ollies];
  for (int i = 0; i < amount_of_ollies; i++)
    ollies[i] = new Ollie();
}

void draw()
{
  for (int i = 0; i < amount_of_ollies; i++)
  {
    ollies[i].update();
    ollies[i].display();
  }
}
