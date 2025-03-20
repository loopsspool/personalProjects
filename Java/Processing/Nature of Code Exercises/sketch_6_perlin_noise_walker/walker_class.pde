class walker
{
  float x, y;
  float xoff, yoff;
  
  walker()
  {
    x = width/2;
    y = height/2;
    
    xoff = 0;
    yoff = 100;
  }
  
  void display()
  {
    fill(50, 20);
    circle(x, y, 16);
  }
  
  void step()
  {
    // NOISE BASED STEPS
    //x = map(noise(xoff), 0, 1, 0, width);
    //y = map(noise(yoff), 0, 1, 0, height);
    
    // NOISE BASED STEP SIZE
    x += map(noise(xoff), 0, 1, -5, 5);
    y += map(noise(yoff), 0, 1, -5, 5);
    
    xoff += 0.01;
    yoff += 0.01;
  }
}
