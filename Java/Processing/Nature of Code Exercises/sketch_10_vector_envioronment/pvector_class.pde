class PVector
{
  float x;
  float y;
  
  PVector(float x_, float y_)
  {
    x = x_;
    y = y_;
  }
  
  float mag()
  {
    return sqrt(x*x + y*y);
  }
  
  void add(PVector v)
  {
    x = x + v.x;
    y = y + v.y;
  }
  
  void sub(PVector v)
  {
    x = x - v.x;
    y = y - v.y;
  }
  
  void mult(float n)
  {
    x *= n;
    y *= n;
  }
  
  void div(float n)
  {
    x /= n;
    y /= n;
  }
  
  void normalize()
  {
    float m = mag();
    if (m != 0)
      div(m);
  }
  
}
