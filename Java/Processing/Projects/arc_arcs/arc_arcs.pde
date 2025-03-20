// arc_arcs
// A buncha arcs stemming from a certain location

// Ethan Jones
// 9-12-19

arcc arc_array;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100, 100);
  
  arc_array = new arcc(width/2, height/2, 30, 50);
}

void draw()
{
  arc_array.display();
}
