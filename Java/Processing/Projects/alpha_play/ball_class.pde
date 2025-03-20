class Ball
{
  // x & y coordinates
  int x;
  int y;
  // x & y diameters
  int x_d;
  int y_d;
  // x & y velocities
  int x_v;
  int y_v;
  
  Ball(int par_x, int par_y, int par_x_d, int par_y_d, int par_x_v, int par_y_v)
  {
    x = par_x;
    y = par_y;
    x_d = par_x_d;
    y_d = par_y_d;
    x_v = par_x_v;
    y_v = par_y_v;
  }
  
  Ball()
  {
    x = 0;
    y = 0;
    x_d = 10;
    y_d = 10;
    x_v = 1;
    y_v = 1;
  }
  
  void display()
  {
    fill(360);
    ellipse(x, y, x_d, y_d);
  }
  
  void move()
  {
    // if ball gonna hit the sides, reverse direction
    if (dist(x, y, width, y) <= x_d/2 || dist(x, y, 0, y) <= x_d/2)
      x_v *= -1;
    // if ball gonna hit the top/bottom, reverse direction
    if (dist(x, y, x, 0) <= y_d/2 || dist(x, y, x, height) <= y_d/2)
      y_v *= -1;
    x += x_v;
    y += y_v;
  }
}
