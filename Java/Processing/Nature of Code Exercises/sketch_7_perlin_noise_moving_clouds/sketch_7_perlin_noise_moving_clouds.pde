float offset_val = 0.0;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 0, 0);

  noiseDetail(5);

}

// TODO: Figure out how to change looks of clouds in between each frame
void draw()
{
  float x_off = offset_val;
  
  loadPixels();
  for (int x = 0; x < width; x++)
  {
    float y_off = offset_val;
    for (int y = 0; y < height; y++)
    {
      float bright = map(noise(x_off, y_off), 0, 1, 0, 360);
      pixels[x+(y*width)] = color(bright);
      y_off += 0.01;
    }
    x_off += 0.01;
  }
  updatePixels();
  
  // movement
  offset_val += 0.015;
}
