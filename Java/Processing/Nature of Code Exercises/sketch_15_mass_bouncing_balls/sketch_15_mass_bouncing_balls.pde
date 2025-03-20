mover[] movers = new mover[10];
PVector wind = new PVector(0.01, 0);

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  
  for (int i = 0; i < movers.length; i++)
    movers[i] = new mover();
}

void draw()
{
  for (int i = 0; i < movers.length; i++)
  {
    movers[i].apply_force(wind);
    float m = movers[i].mass;
    // Scales gravity according to mass to be more accurate
    PVector gravity = new PVector(0, 0.1 * m);
    movers[i].apply_force(gravity);
    
    // INVISIBLE FORCEFIELD ON RIGHT EDGE OF WINDOW
    if (movers[i].location.x > (2*width)/3)
    {
      PVector forcefield = new PVector(map(movers[i].location.x, (2*width)/3, width, -0.0001, -0.1), 0);
      movers[i].apply_force(forcefield);
    }
    
    movers[i].update();
    movers[i].display();
  }
  
}
