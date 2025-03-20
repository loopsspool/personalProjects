class mover
{
  PVector location;
  PVector velocity;
  PVector acceleration;
  PVector mouse;
  PVector dir;
  
  float speed; // Dictates how fast moves tends towards mouse
  float top_speed;
  int size;
  
  float x_off;
  float y_off;
  
  mover()
  {
    location = new PVector(width/2, height/2);
    velocity = new PVector(0.0, 0.0);
    acceleration = new PVector(0.0, 0.0);
    top_speed = 5;
    
    speed = 0.5; // Dictates how fast moves tends towards mouse
    size = 60;
    
    x_off = 0.0;
    y_off = 100.0;
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
    PVector mouse = new PVector(mouseX, mouseY);
    PVector dir = PVector.sub(mouse, location);  // Gives direction
    
    // Changes magnitude of acceleration based on proximity of mover to mouse
      // To see effects better, increase top_speed
    //speed = map (dir.mag(), 0, width + height, 1, 0);
    
    dir.normalize();  // Makes it easy to scale (spped of acceleration)
    dir.mult(speed);
    
    acceleration = dir;
    
    
    velocity.add(acceleration);
    velocity.limit(top_speed);
    location.add(velocity);
  }
  
  void display()
  {
    fill(200);
    circle(location.x, location.y, size);
  }
}
