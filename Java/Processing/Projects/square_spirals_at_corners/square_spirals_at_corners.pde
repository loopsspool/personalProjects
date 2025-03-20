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
  // TOP LEFT CORNER
  pushMatrix();
  translate(0, 0);
  rotate(radians(rotate_acc));
  square(0, 0, size);
  popMatrix();
  
  // TOP RIGHT CORNER
  pushMatrix();
  translate(width, 0);
  rotate(radians(rotate_acc));
  square(0, 0, size);
  popMatrix();

  // BOTTOM LEFT CORNER
  pushMatrix();
  translate(0, height);
  rotate(radians(rotate_acc));
  square(0, 0, size);
  popMatrix();
  
  // BOTTOM RIGHT CORNER
  pushMatrix();
  translate(width, height);
  rotate(radians(rotate_acc));
  square(0, 0, size);
  popMatrix();  
  
  size += 1.3;
  rotate_acc += 1;
  
  if (size >= height)
  {
    stop();
  }
}
