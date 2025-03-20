void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  noStroke();
  
  //frameRate(20);
  background(100);
}

void draw()
{
  // TRANSPARENT BACKGROUND
  push();
  fill(100, 20);
  //rect(0, 0, width, height);
  pop();
  
  
  // COORDINATES
  float plane_sd = 90;
  float plane_mean = height/2;
  float x_gauss = randomGaussian();
  float y_gauss = randomGaussian();
  
  float x = (plane_sd * x_gauss) + plane_mean;
  float y = (plane_sd * y_gauss) + plane_mean;
  
  
  // SIZE
  float size_sd = 20;
  float size_mean = 20;
  float size_gauss = randomGaussian();
  
  float size = (size_sd * size_gauss) + size_mean;
  
  
  // COLOR
  float color_sd = 100;
  float color_mean = 100;
  float color_gauss = randomGaussian();
  
  float col = (color_sd * color_gauss) + color_mean;
  
  
  fill(int(col));
  circle(x, y, size);
}
