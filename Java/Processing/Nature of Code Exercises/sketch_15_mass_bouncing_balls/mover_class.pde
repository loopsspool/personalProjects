class mover
{
  PVector location;
  PVector velocity;
  PVector acceleration;
  
  float mass;
  
  mover()
  {
    location = new PVector(0, random(height));
    velocity = new PVector(0.0, 0.0);
    acceleration = new PVector(0.0, 0.0);
    
    mass = random(1, 10);
  }
  
  void apply_force(PVector force)
  {
    PVector f = PVector.div(force, mass);
    acceleration.add(f);
  }
  
  void check_edges()
  {
    if (location.x > width)
    {
      location.x = width;
      velocity.x *= -1;
    }
    if (location.x < 0)
    {
      location.x = 0;
      velocity.x *= -1;
    }
      
    if (location.y > height)
    {
      location.y = height;
      velocity.y *= -1;
    }
  }

  void update()
  {
    velocity.add(acceleration);
    location.add(velocity);
    check_edges();
    // Resets acceleration so forces don't accumulate
    acceleration.mult(0);
  }
  
  void display()
  {
    fill(200);
    circle(location.x, location.y, mass * 16);
  }
}
