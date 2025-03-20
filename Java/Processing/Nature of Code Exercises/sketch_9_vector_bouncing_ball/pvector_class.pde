class PVector
{
  float x;
  float y;
  
  PVector(float x_, float y_)
  {
    x = x_;
    y = y_;
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
  
  
}
