class Ollie
{
  PVector acceleration;
  PVector velocity;
  PVector location;
  
  float x_off = 0.0;
  float y_off = 100.0;
  
  color c;
  
  Ollie()
  {
    acceleration = new PVector(0, 0);
    velocity = new PVector(0, 0);
    location = new PVector(0, random(height));
  }
  
  void check_edges()
  {
    if (location.x > width)
      location.x = 0;
    if (location.x < 0)
      location.x = width;
      
    if (location.y > height)
      location.y = 0;
    if (location.y < 0)
      location.y = height;
  }
  
  void update()
  {
    x_off += 0.01;
    y_off += 0.01;
    acceleration.x = noise(x_off);
    acceleration.y = noise(y_off);
    
    velocity.add(acceleration);
    velocity.limit(4);
    location.add(velocity);
    
    check_edges();
    
    c = rachel.get(int(location.x), int(location.y));
  }
  
  void display()
  {
    fill(c, 85);
    noStroke();
    
    circle(location.x, location.y, 16);
  }
}
