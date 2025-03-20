class Star
{
  //VARIABLES
  int x;
  int y;
  
  // CONSTRUCTORS
  Star()
  {
    x = int(random(0, width));
    y = int(random(0, height));
  }
  
  Star(int temp_x, int temp_y)
  {
    x = temp_x;
    y = temp_y;
  }
  
  // FUNCTIONS
  void display()
  {
      ellipse(x, y, random(0,8), random(0,8));
  }
  
  void alter_brightness(int temp_b)
  {
    if (frameCount%90 == 0)
     fill(47, 26, temp_b);
  }
}
