class Balloon
{
  PVector location;
  PVector velocity;
  PVector acceleration;
  
  PVector wind;
  
  float x_t;
  float y_t;
  
  Balloon()
  {
    location = new PVector(width/2, height);
    velocity = new PVector(0, 0);
    acceleration = new PVector(0, -0.3);
    
    x_t = 0.0;
    y_t = 100.0;
    
    wind = new PVector(noise(x_t), noise(y_t));
  }

  void check_edges()
  {
    if (location.x < -5)
      location.x = 0;
    if (location.x > width)
      location.x = width;
      
    if (location.y <= 0)
    {
      // If the balloon reaches the top of the screen, "reset" the animation
      location.y = height;
    }

  }

  void update()
  {
    x_t += 0.1;
    y_t += 0.1;
    wind.x = map(noise(x_t), 0, 1, -0.3, 0.3);
    wind.y = map(noise(y_t), 0, 1, -0.1, -0.3);
    
    acceleration.add(wind);
    velocity.add(acceleration);
    velocity.limit(3);
    location.add(velocity);
    // Resets acceleration so wind doesn't accumulate
    acceleration.x = 0;
    acceleration.y = -0.3;
    
    check_edges();
  }
  
  void display()
  {
    circle(location.x, location.y, 30);
  }
  
}
