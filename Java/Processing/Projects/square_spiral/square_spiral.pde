float size = 1;
float rotate_acc = 0;

void setup()
{
  size (800, 800);
  colorMode(HSB, 360, 100, 100);
  noFill();
  
  rectMode(CENTER);
}

void draw()
{
  translate(width/2, height/2);
  
  rotate(radians(rotate_acc));
  square(0, 0, size);
  
  size += 0.92;
  rotate_acc += 1;
}
