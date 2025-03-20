int cols, rows;
int scale = 40;

void settings()
{
  // Setting ssketch window to left side of screen
  // -70 accounts for navigation bar
  size(int(displayWidth/2), int(displayHeight), P3D);
  cols = width / scale;
  rows = height / scale;
}

void setup()
{
  surface.setLocation(0, 0);
  frameRate(1);
  
  colorMode(HSB, 360, 100, 100, 100);
  noStroke();
  background(360);
    
  noLoop();
}

float scaled_x = 0;
float scaled_y = 0;
float scaled_next_y = 0;
float curr_dist_from_hole = 0;
float next_dist_from_hole = 0;
float curr_z = 0;
float next_z = 0;
float highest_dist_from_hole_can_be = sqrt(sq(width/2) + sq(height/2));
void draw()
{
  fill(360);
  stroke(1);
  
  translate(width/2, height/2);
  rotateX(PI/3);
  translate(-width/2, -height/2);

  for (int y=0; y<cols; y++)
  {
    scaled_y = y*scale;
    scaled_next_y = (y+1)*scale;
    beginShape(TRIANGLE_STRIP);
    for (int x=0; x<cols; x++)
    {
      scaled_x = x*scale;
      // TODO: Too gradual, want a much steeper curve just in the center
      // TODO: Set variable to easily switch between triangle strip and regular rects to see which I like better
      curr_dist_from_hole = dist(width/2, height/2, x*scale, y*scale);
      //curr_z = map(curr_dist_from_hole, highest_dist_from_hole_can_be, 0, 0, -40);
      //next_dist_from_hole = dist(width/2, height/2, x*scale, (y+1)*scale);
      //next_z = map(next_dist_from_hole, highest_dist_from_hole_can_be, 0, 0, -40);
      
      // Below is interesting, but makes it too round
      // TODO: Maybe if within radius rotate to center of hole?
      //if (curr_dist_from_hole <= 180)
      if ((scaled_x > (2*width/5)) && (scaled_x < (3*width/5)) && (scaled_y > (2*height/5)) && (scaled_y < (3*height/5)))
      {
        curr_z = y * -30;
        next_z = (y+1) * -30;
        //curr_dist_from_hole = dist(width/2, height/2, x*scale, y*scale);
        //curr_z = map(curr_dist_from_hole, height/5, 0, -20, -600);
        //next_dist_from_hole = dist(width/2, height/2, x*scale, (y+1)*scale);
        //next_z = map(next_dist_from_hole, height/5, 0, -20, -600);
      }
      vertex(scaled_x, scaled_y, curr_z);
      vertex(scaled_x, scaled_next_y, next_z);
      //rect(x*scale, y*scale, scale, scale);
      curr_z = 0;
      next_z = 0;
    }
    endShape();
  }
}
