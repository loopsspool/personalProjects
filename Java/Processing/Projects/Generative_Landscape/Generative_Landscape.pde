float x_off, y_off;  // For noise
int scale;  // Size of strips
int rows, cols;
int w, h;  // Not actually width and height but bigger so mountains still extend to edges after rotation

float[][] z_vals;  // Mountain z (height) values

PVector sunlight_dir;  // Direction of sunlight
float sunlight_x_acc, sunlight_y_acc;  // Controls sun movement
color sun_color;

void setup()
{
  size(900, 900, P3D);
  surface.setLocation(100, 50);
  colorMode(HSB, 360, 100, 100, 100);
  sun_color = color(310, 100, 100);
  
  scale = 15;
  // Bigger than width and height so mountains still extend to edges after rotation
  w = width * 2;
  h = height * 2;
  rows = h / scale;
  cols = w / scale;
  
  z_vals = new float[cols][rows];
  float y_off = 10.0;
  for (int y = 0; y < rows; y++)
  {
    float x_off = 0.0;
    for (int x = 0; x < cols; x++)
    {
      z_vals[x][y] = map(noise(x_off, y_off), 0, 1, -300, 300);
      
      x_off += 0.05;
    }
    y_off += 0.05;
  }
  
  // Creating vector for sunlight origin and direction
  sunlight_dir = new PVector(-1, 0, 0.1);
  directionalLight(hue(sun_color), saturation(sun_color), brightness(sun_color), sunlight_dir.x, sunlight_dir.y, sunlight_dir.z);
  sunlight_x_acc = 0.002;
  sunlight_y_acc = sunlight_x_acc * 6;
}

void draw()
{
  // Sun
  //pointLight(64, 30, 100, -width/2, 0, 100);
  //sunlight_dir.x = mouseX - width/2;
  //sunlight_dir.y = mouseY - width/2;
  // Moves sun across x-axis (moving East to West)
  sunlight_dir.x += sunlight_x_acc;
  // Resets sun if its at far left
    // gets really slow at end if set to 1
  if (sunlight_dir.x > 0.99)
  {
    sunlight_dir.x = -1;
    sunlight_dir.z = 0.1;
  }
  // Moves sun slightly on y-axis (mimics it rising)
    // Can't map bc it breaks for some reason
  // sunlight_y_acc adds to z because of rotation... z kinda takes place of y
  if (sunlight_dir.x <= 0)
    sunlight_dir.z -= sunlight_y_acc;
  if (sunlight_dir.x > 0)
    sunlight_dir.z += sunlight_y_acc;
    
  // Normalized so I can think in terms of vectors, but directionalLgiht expects normalized vector
  sunlight_dir.normalize();
  directionalLight(hue(sun_color), saturation(sun_color), brightness(sun_color), sunlight_dir.x, sunlight_dir.y, sunlight_dir.z);

  background(color(200, 75, 100));
  //fill(color(277, 100, 25));
  //stroke(color(277, 100, 10));
  noStroke();
  
  push();
  translate(width/2, height/2);  // Draw to (and rotate around) center of window
  rotateX(PI/3);  // Angles so looking at mountains from semi-birds-eye view
  // Allows things to be drawn in the top left of the window after rotateX(PI/3);
  translate(-w/2, -h/2);
  
  // Sun display
  push();
  emissive(hue(sun_color), saturation(sun_color), brightness(sun_color));
  float sun_x = map(sunlight_dir.x, -1, 1, w, 0);
  float sun_z = map(sunlight_dir.z, 0.1, -1, -h/10, h/7);
  // -100 y so sun doesn't clip through mountains at back
  translate(sun_x, -100, sun_z);
  sphere(80);
  pop();
  
  // Mountain colors
  fill(112, 50, 100);
  
  for (int y = 0; y < rows - 1; y++)
  {
    beginShape(TRIANGLE_STRIP);
    for (int x = 0; x < cols; x++)
    {
      // Fill mapped of Zheight for illusion of shading
      //fill(112, 50, map(z_vals[x][y], -300, 300, 0, 100));
      vertex(x * scale, y * scale, z_vals[x][y]);
      // y + 1 to add vertex below so triangle strips works
      vertex(x * scale, (y + 1) * scale, z_vals[x][y+1]);
    }
    endShape();
  }
  pop();
}
