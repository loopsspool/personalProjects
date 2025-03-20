float x_off =0; 
PVector location;
PVector velocity;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  
  location = new PVector(width/2, height/2);
  velocity = new PVector(2.5, 5);
}

void draw()
{
  push();
  fill(255, 50);
  rect(0, 0, width, height);
  pop();
  
  location.add(velocity);
  
  if ((location.x > width) || (location.x < 0))
    velocity.x *= -1;
  if ((location.y > height) || (location.y < 0))
    velocity.y *= -1;
    
  circle(location.x, location.y, 32);
}
