// Asteroids inch through space carried solely by the momentum

class asteroid
{
  PImage asteroid_img;
  int size;
  float rotation;
  // Accumulator changing rotation each loop
  float rotation_acc;
  
  PVector acceleration;
  PVector velocity;
  PVector location;
  
  float top_speed;
  
  asteroid()
  {
    asteroid_img = loadImage("Asteroid.png");
    size = int(random(40, 80));
    top_speed = random(0.5, 1.5);
    
    float x_decider = random(-1, 1);  // Decides if asteroid will move left or right
    float y_decider = random(-1, 1);  // Decides if asteroid will move up or down
    location = new PVector(random(width), random(height));
    velocity = new PVector(0, 0);  

    // Determining asteroid directions
    if (x_decider >= 0)
    {
      if (y_decider >= 0)
        acceleration = new PVector(random(0.25, 4), random(1, 3));
      else
        acceleration = new PVector(random(0.25, 4), random(-1, -3));
    }
    else
    {
      if (y_decider >= 0)
        acceleration = new PVector(random(-0.25, -4), random(1, 3));
      else
        acceleration = new PVector(random(-0.25, -4), random(-1, -3));
    }
    
    rotation = 0;
    // Rotation shall be different for each asteroid
    rotation_acc = radians(random(-1, 1));
  }
  
  void check_edges()
  {
    // Resets image if outside boundaries
      // Boundaries and reset based on image width so transition is smooth
    if (location.x > width + asteroid_img.width)
      location.x = -asteroid_img.width;
    if (location.x < -asteroid_img.width)
      location.x = width + asteroid_img.width;
      
    if (location.y > height + asteroid_img.width)
      location.y = -asteroid_img.width;
    if (location.y < -asteroid_img.width)
      location.y = height + asteroid_img.width;
  }

  void update()
  {
    // Causing movement
    velocity.add(acceleration);
    velocity.limit(top_speed);
    location.add(velocity);
    
    rotation += rotation_acc;
    
    check_edges();
  }
  
  void display()
  {
    push();
    // Rotate origin by default is (0, 0), changing this gives object rotation about itself
    translate(location.x, location.y);
    rotate(rotation);
    image(asteroid_img, 0, 0, size, size);
    pop();
  }
}
