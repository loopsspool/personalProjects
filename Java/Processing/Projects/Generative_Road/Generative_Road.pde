float x_off, y_off;  // For mountain noise
float road_x_off;  // For road noise
float[][] road_points;  // x, y, z of road points
int scale;  // Size of strips
int rows, cols;
int w, h;  // Not actually width and height but bigger so mountains still extend to edges after rotation

float flying = 0;
float[][] z_vals;  // Mountain z (height) values

int road_index;  // Selects which vertices to draw the road on
int road_scale;
int road_raise;  // Sets houw much higher road is above mountains (so doesn't get clipped)
float road_noise_acc;
int road_noise_range;
int yellow_line_raise;
float yellow_line_buffer;

void setup()
{
  size(900, 900, P3D);
  surface.setLocation(100, 50);
  colorMode(HSB, 360, 100, 100, 100);
  
  scale = 15;
  // Bigger than width and height so mountains still extend to edges after rotation
  w = int(width * 2.1);
  h = height * 2;
  rows = h / scale;
  cols = w / scale;
  
  z_vals = new float[cols][rows];
  // Initializing z values
  for (int y = 0; y < rows; y++)
  {
    x_off = 0.0;
    for (int x = 0; x < cols; x++)
    {
      z_vals[x][y] = map(noise(x_off, y_off), 0, 1, -200, 200);
      
      x_off += 0.04;
    }
    y_off += 0.04;
  }
  
  road_points = new float[rows][3];
  road_index = floor(random(cols));
  road_x_off = 0.0;
  road_noise_acc = 0.2;
  road_noise_range = 3;
  road_scale = 12;
  road_raise = int(road_scale / 5);
  yellow_line_buffer = road_scale/10;
  for (int y = 0; y < rows - 1; y++)
  {
    road_x_off += road_noise_acc;
    road_index += int(map(noise(road_x_off), 0, 1, -road_noise_range, road_noise_range));
    if (road_index > cols - 1)
      road_index = cols - 1;
    if (road_index < 0)
      road_index = 0;
    
    road_points[y][0] = road_index * scale;
    road_points[y][1] = y * scale;
    road_points[y][2] = z_vals[road_index][y] + road_raise;
  }
}

void draw()
{
  flying -= 0.005;
  y_off = flying;
  
  // Framecount conditional so update doesn't happen too quick and the whole window becomes the same
  if(frameCount % 4 == 0)
  {
    for (int y = rows - 1; y > 0; y--)
    {
      for (int x = 0; x < cols; x++)
      {
        // Setting next mountain row height to previous mountain row height
        z_vals[x][y] = z_vals[x][y-1];
      }
      // Sets next road points to previous road points
      // Only update the x and the z values, otherwiwse gets bugged
      road_points[y][0] = road_points[y-1][0];
      //road_points[y][1] = road_points[y-1][1];
      road_points[y][2] = road_points[y-1][2];
    }
  }
  
  // Sets new mountain row height
  x_off = 0.0;
  for (int x = 0; x < cols; x++)
  {
    z_vals[x][0] = map(noise(x_off, y_off), 0, 1, -200, 200);
    
    x_off += 0.04;
  }
  y_off += 0.04;
  
  // Sets new road height
  if (frameCount % 4 == 0)
  {
    road_x_off += road_noise_acc;
    road_index += int(map(noise(road_x_off), 0, 1, -road_noise_range, road_noise_range));
    if (road_index > (4 * cols)/5)
      road_index = (4 * cols)/5;
    if (road_index < cols/5)
      road_index = cols/5;
    
    road_points[0][0] = road_index * scale;
    road_points[0][1] = 0 * scale;
    road_points[0][2] = z_vals[road_index][0] + road_raise;
  }
  
  background(color(200, 75, 100));
  //fill(color(277, 100, 25));
  //stroke(color(277, 100, 10));
  noStroke();

  translate(width/2, height/2);  // Draw to (and rotate around) center of window
  rotateX(PI/4);  // Angles so looking at mountains from semi-birds-eye view
  // Allows things to be drawn in the top left of the window after rotateX(PI/3);
  translate(-w/2, -h/2);
  
  for (int y = 0; y < rows - 1; y++)
  {
    beginShape(TRIANGLE_STRIP);
    for (int x = 0; x < cols; x++)
    {
      // Fill mapped of Zheight for illusion of shading
      fill(112, 50, map(z_vals[x][y], -200, 200, 0, 100));
      vertex(x * scale, y * scale, z_vals[x][y]);
      // y + 1 to add vertex below so triangle strips works
      vertex(x * scale, (y + 1) * scale, z_vals[x][y+1]);
    }
    endShape();
  }
  
  // TODO: Try changing to a bunch of little arcs so can map color on smaller scale like with mountains
  push();
  noFill();
  stroke(150);
  strokeWeight(road_scale);
  // Road
  beginShape();
  for (int y = 0; y < rows - 1; y++)
  {
    curveVertex(road_points[y][0], road_points[y][1], road_points[y][2]);
  }
  endShape();
  // Yellow lines
  strokeWeight(road_scale / 10);
  stroke(50, 40, 75);
  beginShape();
  for (int y = 0; y < rows - 1; y++)
  {
    float yellow_line_y = road_points[y][1] - yellow_line_raise;
    curveVertex(road_points[y][0] - yellow_line_buffer / 2, yellow_line_y, road_points[y][2]);
  }
  endShape();
  beginShape();
  for (int y = 0; y < rows - 1; y++)
  {
    float yellow_line_y = road_points[y][1] - yellow_line_raise;
    curveVertex(road_points[y][0] + yellow_line_buffer / 2, yellow_line_y, road_points[y][2]);
  }
  endShape();
  pop();
}
