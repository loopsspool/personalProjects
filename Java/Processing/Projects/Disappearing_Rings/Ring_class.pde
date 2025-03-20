class Ring
{
  int ww;
  int wh;
  int x;
  int y;
  int OG_y;
  int y_min;
  int w;
  int OG_w;
  int h;
  float start;
  float end;
  color col;
  // Place when ring "dies"
  int ring_end;
  
  Ring(int par_ww, int par_wh, int par_y_min, int par_x, int par_y, int par_w, int par_h, float par_start, float par_end, color par_col)
  {
    ww = par_ww;
    wh = par_wh;
    x = par_x;
    y = par_y;
    OG_y = par_y;
    y_min = par_y_min;
    w = par_w;
    OG_w = par_w;
    h = par_h;
    start = par_start;
    end = par_end;
    col = par_col;
    
    ring_end = wh;
  }
  
  void move()
  {
    if (y == ring_end)
    {
      y = y_min;
      // This next line is done so transparency based off original y start will work
      // and when it resets to the hightest y point transparency will work as expected
      OG_y = y_min;
    }
      
    y++;
  }
  
  void display()
  {
    // Change opacity based on y value
    stroke(col, map(y, OG_y, ring_end, 100, 0));
    // Change width based on y value
    w = floor(map(y, OG_y, ring_end, OG_w, 800));
    // Actually display
    arc(x, y, w, h, start, end);
  }
}
