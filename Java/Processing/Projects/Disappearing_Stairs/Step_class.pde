class Step
{
  int ww;
  int wh;
  float x1;
  float OG_x1;
  int y;
  int OG_y;
  int y_min;
  float x2;
  float OG_x2;
  // width incrementer for step
  float w_inc;
  float vel;
  color col;
  // Place when step "dies"
  int step_end;
  
  Step(int par_ww, int par_wh, int par_y_min, float par_x1, int par_y, float par_x2, float par_w_inc, float par_vel, color par_col)
  {
    ww = par_ww;
    wh = par_wh;
    x1 = par_x1;
    OG_x1 = par_x1;
    y = par_y;
    OG_y = par_y;
    y_min = par_y_min;
    x2 = par_x2;
    OG_x2 = par_x2;
    w_inc = par_w_inc;
    vel = par_vel;
    col = par_col;
    
    step_end = wh;
  }
  
  void move()
  {
    if (y >= step_end)
    {
      y = y_min;
      // This next line is done so transparency based off original y start will work
      // and when it resets to the hightest y point transparency will work as expected
      OG_y = y_min;
      // Reset original size of steps, too
      x1 = OG_x1;
      x2 = OG_x2;
    }
      
    y += vel;
  }
  
  void display()
  {
    // Change opacity and step width based on y value
    if (y < wh/2)
    {
      // Fade in
      stroke(col, map(y, 0, wh/2, 0, 100));
      // increase size of step
      x1 -= w_inc;
      x2 += w_inc;
    }
    else
    {
      // Fade out
      stroke(col, map(y, wh/2, step_end, 100, 0));
      // decrease size of step
      x1 += w_inc;
      x2 -= w_inc;
    }

    // Actually display
    line(x1, y, x2, y);
  }
}
