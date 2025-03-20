// Definitely overengineered lol
// And making the spiderweb class was an afterthought and a workaround
  // So it is a sloppy class...
void setup()
{
  size(780, 123);
  surface.setLocation(50, 50);
  
  colorMode(HSB, 360, 100, 100, 100);
  background(0);
  noLoop();
}

void draw()
{
  Spiderweb ul_spiderweb = new Spiderweb(0, 0);
  Spiderweb lr_spiderweb = new Spiderweb(width - 1, height);
  ul_spiderweb.display();
  lr_spiderweb.display();
  
}

class Spiderweb
{
  float origin_x;
  float origin_y;
  
  Spiderweb(float x, float y)
  {
    origin_x = x;
    origin_y = y;
  }
  
  void display()
  {
    push();
    stroke(360);
    noFill();
    strokeWeight(3);
    int circle_d = 30;
    translate(origin_x, origin_y);
    circle(0, 0, circle_d);
    
    int main_strings = 8;
    float rotation = 0;
    float[] rotation_array;
    rotation_array = new float [main_strings];
    // Main strings
    push();
      for (int i = 0; i < main_strings; i++)
      {
        // Adds a bit of randomness but makes it difficult to work around
        //rotation = radians(360/(main_strings + random(-4, 4)));
        rotation = radians(360/main_strings);
        rotation_array[i] = rotation;
        rotate(rotation);
        line(0, -circle_d/2, 0, -width);
      }
    pop();
    
    // Curves in between main strings
    for (int i = 0; i < main_strings; i++)
    {
      if (i == main_strings - 1)
      {
        // draw arc from [i] to [0]
        break;
      }
      else
      {
        // Puts axis at current main line
        rotate(rotation_array[i]);
        push();
          // Puts axis halfway between current main line and next
            // Negated by pop(), so will hop back to current main line so rotate will be accurate still
          rotate(rotation_array[i+1]/2);
          translate(0, -circle_d/2);
          
          // The below method works
            // Only drawback is get() will go offscreen after rotate call
              // This means it'll always return black, resulting in an infinite loop
                // Tho could do an arc amount check and after it gets to a certain number
                  // Add 25. x looks close to adding 20 + (loop_acc * 4)
          int y_base = 0;
          int y_inc = 0;  // Changes the incrementer value so it doesn't look so "perfect"
          int loop_acc = 0;
          for (int y = -y_base; y > -height * 1.5; y -= y_base + y_inc)
          {
            int x = 0;
            while(get(int(screenX(x, y)), int(screenY(x, y))) == color(0))
            {
              x++;
            }
            //x += 20 + (4 * loop_acc);
            //println(x);
  
            stroke(360);
            beginShape();
              // First and fifth vertices are control points
              curveVertex(-x, y);
              curveVertex(-x, y);
              curveVertex(0, y * 0.8);
              curveVertex(x, y);
              curveVertex(x, y);
            endShape();
            
            y_inc += 10;
            loop_acc++;
          }
        pop();
      }
    }
  pop();
  }
}
