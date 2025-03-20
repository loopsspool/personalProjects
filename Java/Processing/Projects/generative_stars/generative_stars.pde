import java.util.ArrayList;
import java.util.Random;

int STAR_SIZE = 100;
int STAR_POINTS;
float INNER_CURVE_ANGLE;
float OUTER_CURVE_ANGLE;
int HIGHEST_POINTS_NUM = 12;
float OUTLINE_SIZE_MULTIPLIER = 1.5;
int OUTLINE_SIZE = floor(STAR_SIZE * OUTLINE_SIZE_MULTIPLIER);
int[] OUTLINE_POINTS;

void setup()
{
  size(800, 800);
  surface.setLocation(50, 50);
  colorMode(HSB, 360, 100, 100, 100);
  //noLoop();
  frameRate(1);
  
  strokeWeight(2);
  //curveTightness(-1);
  
  OUTLINE_POINTS = new int[]{3, 4, 6, 8, 10, 12, 14, 16};
}

void draw()
{
  background(255);
  push();
    translate(width/2, height/2);
    star();
    point_lines();
    //outline_shape();
  pop();
}

// Courtesy of https://processing.org/examples/star.html
  // Modified a bit to make curved stars
void star() 
{
  // Amount of star points
  STAR_POINTS = floor(random(3, HIGHEST_POINTS_NUM));
  // Where the curve occurs (Larger parameter moves curves closer to outside, smaller to inside)
  int curve_point = floor(random(-STAR_SIZE, STAR_SIZE)/2);
  
  int loop_acc = 0;
  float angle = radians(360 / float(STAR_POINTS));
  float half_angle = angle/2.0;
  float sx;
  float sy;
  
  INNER_CURVE_ANGLE = random(half_angle/4, 10 * half_angle);
  OUTER_CURVE_ANGLE = radians(random(TWO_PI));
  
  noFill();
  beginShape();
    // + (2 * angle) to give the final curve a natural finish (by adding another that draws over)
    for (float a = angle; a <= TWO_PI  + (2 * angle); a += angle)
    {
      loop_acc++;
      
      // Setting inner points
      // If it's the first point, this conditional sets it so its not at a corner
        // or middle of an arc so the curve doesn't sharpen at a point
      if (a == angle)
      {
        sx = cos((a - half_angle/1.1) - INNER_CURVE_ANGLE) * curve_point;
        sy = sin((a - half_angle/1.1) - INNER_CURVE_ANGLE) * curve_point;
      }
      else
      {
        // To change angle of star where it meets the center, change what's after a- eg (a-(half_angle/16))
          // If bigger positive multiples, the fingers look more like leaves (a-(10 * half_angle))
        // Also potentially changing independantly
        sx = cos(a - INNER_CURVE_ANGLE) * curve_point;
        sy = sin(a - INNER_CURVE_ANGLE) * curve_point;
      }
      curveVertex(sx, sy);
        
      // Outtermost points
      // To change angle of outtermost star points, change what's after a eg (a-1)
      sx = cos(a - OUTER_CURVE_ANGLE) * STAR_SIZE/2;
      sy = sin(a - OUTER_CURVE_ANGLE) * STAR_SIZE/2;
      curveVertex(sx, sy);
      
      // Drawing the final curve
      if (loop_acc >= (STAR_POINTS + 1))
      {
        sx = cos((a + half_angle/1.1) - INNER_CURVE_ANGLE) * curve_point;
        sy = sin((a + half_angle/1.1) - INNER_CURVE_ANGLE) * curve_point;
        curveVertex(sx, sy);

        // DO NOT TAKE THIS OUT
        // Otherwise the loop will continue and draw a wrong line
        break;
      }
    }
  endShape();
}

void point_lines() 
{
  float angle = radians(360 / float(STAR_POINTS));
  float sx1;
  float sy1;
  float sx2;
  float sy2;
  float sx3;
  float sy3;
  float sx4;
  float sy4;

  //OUTER_CURVE_ANGLE = radians(random(TWO_PI));
  float start_point_scale = random(0, OUTLINE_SIZE_MULTIPLIER - 0.5);
  float end_point_scale = random(OUTLINE_SIZE_MULTIPLIER - 0.5, OUTLINE_SIZE_MULTIPLIER - 0.1);
  float end_anchor_x = random(-0.1, 0.1);
  float end_anchor_y = random(-0.1, 0.1);
  
  noFill();
    for (float a = angle; a <= TWO_PI + angle; a += angle)
    {
      //sx1 = cos(a - INNER_CURVE_ANGLE) * (start_point * STAR_SIZE/2);
      //sy1 = sin(a - INNER_CURVE_ANGLE) * (start_point * STAR_SIZE/2);
      sx1 = 0;
      sy1 = 0;
      sx2 = cos(a - INNER_CURVE_ANGLE) * (start_point_scale * STAR_SIZE/2);
      sy2 = sin(a - INNER_CURVE_ANGLE) * (start_point_scale * STAR_SIZE/2);
      sx3 = cos(a - OUTER_CURVE_ANGLE) * (end_point_scale * STAR_SIZE/2);
      sy3 = sin(a - OUTER_CURVE_ANGLE) * (end_point_scale * STAR_SIZE/2);
      sx4 = cos(a - end_anchor_x) * (end_point_scale * STAR_SIZE/2);
      sy4 = sin(a - end_anchor_y) * (end_point_scale * STAR_SIZE/2);
      curve(sx1, sy1, sx2, sy2, sx3, sy3, sx4, sy4);
    }
}

ArrayList multiples(int points)
{
  ArrayList<Integer> divisible_by = new ArrayList<Integer>();
  
  // Finds all numbers that can divide points number
  for (int i = 2; i <= HIGHEST_POINTS_NUM; i++)
  {
    if (points % i == 0)
      divisible_by.add(i);
  }
  
  return divisible_by;
}

void outline_shape()
{
  strokeWeight(floor(random(1, 6)));
  boolean is_ngon = true_below(0.6);
  // Gets random points number from outline points array
  int rand = new Random().nextInt(OUTLINE_POINTS.length);
  if (is_ngon)
    ngon(OUTLINE_POINTS[rand], OUTLINE_SIZE/2);
  else
    circle(0, 0, OUTLINE_SIZE);
  
}

void ngon(int points, int radius)
{
  // Determines if triangles should be pointing up or down
    // and if squares should be flat or diamonds
  boolean additional_rotate = true_below(0.5);
  
  // Adjusting triangle/square sizes a bit
  if (points == 3)
    radius *= 1.6;
  if (points == 4)
    radius *= 1.2;
    
  float rotate = radians(360/points);
  beginShape();
    for (int i = 0; i < points; i++)
    {
      float angle = i * rotate;
      
      // Potential additional rotate for even ngons
      if (additional_rotate)
      {
        // Makes flat square, not diamond
        if (points == 4)
          angle += rotate/2;
        // Gives even ngon a flat bottom
        if ( (points != 4) && (points % 2 == 0))
          angle += rotate/4;
      }
      
      // Adjusts triangles to point up or down
      if (points == 3)
      {
        if (additional_rotate)
        {
          // Point up
          angle += rotate/4;
        }
        else
        {
          // Point down
          angle += rotate - radians(30);
        }
      }       
      
      float x = cos(angle) * radius;
      float y = sin(angle) * radius;
      vertex(x, y);
    }
  endShape(CLOSE);
}

boolean true_below(float limit)
{
  if (random(1) < limit)
    return true;
  else
    return false;
}
