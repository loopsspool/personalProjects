void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  
  
}

void draw()
{
  background(255);
  
  PVector mouse = new PVector(mouseX, mouseY);
  PVector center = new PVector(width/2, height/2);
  
  mouse.sub(center);
  
  // NORMALIZE
  //mouse.normalize();
  //mouse.mult(50);   // For visibility
  
  translate(width/2, height/2);
  
    // MAGNITUDE VISUALIZATION
  float m = mouse.mag();
  push();
  fill(0);
  if (mouse.x > 0)
    rect(0, -height/2, m, 20);
  if (mouse.x < 0)
    rect(0, -height/2, -m, 20);
  text(m, -5, -height/4);
  pop();
  
  line(0, 0, mouse.x, mouse.y);
}
