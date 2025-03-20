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
  
  // Limits magnitude of velocity
  void limit(float max)
  {
    if (mag() > max)
    {
      normalize();
      mult(max);
    }
  }
  
  void random2D()
  {
    x = random(-1, 1);
    y = random(-1, 1);
    
    normalize();
  }
  
  void noise2D(float x_, float y_)
  {
    x = map(noise(x_), 0, 1, -1, 1);
    y = map(noise(y_), 0, 1, -1, 1);
    
    normalize();
  }
}
