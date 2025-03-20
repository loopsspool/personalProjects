import java.util.Random;

Random generator;

void setup()
{
  size(800, 800);
  generator = new Random();
}

void draw()
{
  float num = randomGaussian();
  float sd = 60;
  float mean = 400;
  
  float x = num * sd + mean;
  
  noStroke();
  fill(0, 10);
  circle(x, 400, 16);
  
}
