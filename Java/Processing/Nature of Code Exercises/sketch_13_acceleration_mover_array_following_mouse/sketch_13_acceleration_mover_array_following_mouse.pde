mover[] movers;
float[] speeds;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  
  int amount = 40;
  
  movers = new mover[amount];
  speeds = new float[amount];
  
  for (int i= 0; i < movers.length; i++)
  {
    movers[i] = new mover();
    // NOISE MOTION
    if (i == 0)
      speeds[i] = map(noise(i), 0, 1, 1, 3);
    else
      speeds[i] = map(noise(i*0.001), 0, 1, 1, 3);
    // RANDOM MOTION
    //speeds[i] = random(1, 3);
  }
}

void draw()
{
  // BACKGROUND
  push();
  fill(0, 30);
  rect(0, 0, width, height);
  pop();
  
  for (int i = 0; i < movers.length; i++)
  {
    movers[i].update(speeds[i]);
    movers[i].display();
  }
}
