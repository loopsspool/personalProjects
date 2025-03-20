class walker
{
  float x;
  float y;
  
  walker()
  {
    x = width/2;
    y = height/2;
  }
  
  void display()
  {
    fill(0);
    circle(x, y, 1);
  }
  
  void step()
  {
    float choice = random(0, 1);
    float x_step = random(0, 1);
    float y_step = random(-1, 1);
    
    if (choice > 0.8)
    {
      if (mouseX > x)
        x++;
      else
        x--;
        
      if (mouseY > y)
        y++;
      else
        y--;
    }
    else
    {
      x += x_step;
      y += y_step;
    }
  }

}
