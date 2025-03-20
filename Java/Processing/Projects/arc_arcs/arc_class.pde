class arcc
{
  boolean direction;
  int x;
  int y;
  int w;
  int h;
  
  arcc(int p_x, int p_y, int p_w, int p_h)
  {
    x = p_x;
    y = p_y;
    w = p_w;
    h = p_h;
  }
  
  void display()
  {
    arc(x, y, w, h, 0, HALF_PI);
  }
}
