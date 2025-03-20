class Ball
{  
  int size;
  int col;
  
  PVector location;
  PVector velocity;
  PVector acceleration;
  
  int top_speed;
  // Controls noise
  float t_x;
  float t_y;
  
  Ball(int size_)
  {
    size = size_;
    col = color(random(0, 360), random(10, 60), 100, 80);
    
    // Limits velocity
    top_speed = 4;
    
    location = new PVector(random(0, width), random(0, height));
    velocity = new PVector(random(-1, 1), random(3, 7));
    acceleration = new PVector(random(-1, 1), random(-1, 1));
    
    t_x = random(0, 1000);
    t_y = random(0, 1000);
    
  }
  
  void check_edges()
  {
    // If goes beyond x boundaries, restart from top
    if (location.x < -size)
    {
      location.x = width;
      location.y = -size;
      col = color(random(0, 360), random(10, 60), 100, 80);
    }
    if (location.x > width + size)
    {
      location.x = 0;
      location.y = -size;
      col = color(random(0, 360), random(10, 60), 100, 80);
    }
      
    // Not needed since particles oonly move down
    //if (location.y < -size)
    //  location.x = height;
    if (location.y > height + size)
    {
      location.y = -size;
      col = color(random(0, 360), random(10, 60), 100, 80);
    }
  }
  
  void update()
  {
    t_x += 0.1;
    t_y += 0.1;
    // Changes acceleration each frame to make squiggles
    acceleration.x = map(noise(t_x), 0, 1, -0.5, 0.5);
    acceleration.y = map(noise(t_y), 0, 1, 0.1, 0.3);
    
    // Creating movement
    velocity.add(acceleration);
    velocity.limit(top_speed);
    location.add(velocity);
    
    check_edges();
  }
  
  void display()
  {
    fill(col);
    circle(location.x, location.y, size);
  }
}
