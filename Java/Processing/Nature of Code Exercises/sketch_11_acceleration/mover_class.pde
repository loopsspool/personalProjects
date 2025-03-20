class mover
{
  PVector location;
  PVector velocity;
  PVector acceleration;
  
  float top_speed;
  int size = 60;
  
  float x_off = 0.0;
  float y_off = 100.0;
  
  mover()
  {
    location = new PVector(width/2, height/2);
    velocity = new PVector(0.0, 0.0);
    acceleration = new PVector(0.0, 0.0);
    top_speed = 5;
  }
  
  void check_edges()
  {
    if (location.x > width + size/2)
      location.x = 0;
    else if (location.x < -size/2)
      location.x = width;
      
    if (location.y > height + size/2)
      location.y = 0;
    else if (location.y < -size/2)
      location.y = height;
  }
  
  void arrow_key_accel()
  {
    if (keyPressed)
    {
      // If UP pressed, accelerate
      if (keyCode == UP)
      {
        acceleration.x -= 0.003;
        acceleration.y -= 0.003;
      }
      
      // If DOWN pressed, brake
      if (keyCode == DOWN)
      {
        acceleration.x += 0.0001;
        acceleration.y += 0.0001;
      }
    }
    else
    {
      acceleration.x = 0.0;
      acceleration.y = 0.0;
    }
  }
  
  void update()
  {
    // ARROW KEY ACCELERATION
    //arrow_key_accel();
    x_off += 0.03;
    y_off += 0.03;
    
    // NOISE ACCELERATION
    //acceleration.noise2D(x_off, y_off);
    
    // RANDOM ACCELERATION
    acceleration.random2D();
    // Scales random values since random2D returns unit vector
    acceleration.mult(random(-2, 2));
    velocity.add(acceleration);
    velocity.limit(top_speed);
    location.add(velocity);
  }
  
  void display()
  {
    fill(200);
    circle(location.x, location.y, size);
    
    fill(0);
    //Left eye
    circle(location.x - size/4, location.y - (size/8 + 4), size/10);
    // Right eye
    circle(location.x + size/4, location.y - size/12, size/7);
  }
}
