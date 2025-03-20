// Rocketeers are confident, steadfast, and uncompromising

class rocket
{
  PImage rocket_ship_img;
  float rotation;
  float size_scale;  // Scales size of ship
  
  PVector location;
  PVector velocity;
  PVector acceleration;
  
  float top_speed;
  
  rocket()
  {
    rocket_ship_img = loadImage("Rocket Ship RIGHT.png");
    // Scales size of ship
    size_scale = random(0.7, 1.2);
    
    top_speed = random(5, 12);
    
    float decider = random(-1, 1);  // Decides if rocket will move left or right
    location = new PVector(random(width), random(height));
    velocity = new PVector(0, 0);
    // Determining rocket direction
    if (decider >= 0)
      acceleration = new PVector(random(0.25, 4), random(1, 3));
    else
      acceleration = new PVector(random(-0.25, -4), random(1, 3));

    // Heading gives angle of direction of vector
      // So this rotates the rocket so it is facing the direction of its vector
    rotation = acceleration.heading();
  }
  
  void check_edges()
  {
    // Resets image if its outside boundaries
      // Boundaries and reset based on image height so transition is smooth
    if (location.x > width + rocket_ship_img.height)
      location.x = -rocket_ship_img.height;
    if (location.x < -rocket_ship_img.height)
      location.x = width + rocket_ship_img.height;
      
    if (location.y > height + rocket_ship_img.height)
      location.y = -rocket_ship_img.height;
    if (location.y < -rocket_ship_img.height)
      location.y = height + rocket_ship_img.height;
  }
  
  void update()
  {
    // Causing movement
    velocity.add(acceleration);
    velocity.limit(top_speed);
    location.add(velocity);
    
    check_edges();
  }
  
  void display()
  {
    push();
    // Rotate origin by default is (0, 0), changing this gives object rotation about itself
    translate(location.x, location.y);
    rotate(rotation);
    image(rocket_ship_img, 0, 0, 100 * size_scale, 60 * size_scale);
    pop();
  }
}
