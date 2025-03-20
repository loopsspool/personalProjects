// Ethan Jones
// 8-19-19
// Exercise drawing a bunch of squares with the illusion of depth randomly

import java.util.Random;

// random coordinates for boxes
float randX1, randY1;
int amount, depth_boxes;
String depth_side;
String[] depth_side_array;
float side;
float grey;
int draw_frame;

void setup()
{
  size(800, 800);
  colorMode(HSB, 360, 100, 100);
  ellipseMode(CORNER);
  
  stroke(0);
  
  // box size
  side = 30;
  // amount of boxes
  amount = 1;
  // strength of "depth"
  depth_boxes = 30;
  // where depth boxes appear from
  depth_side = "bottom left";
  // sets how often squares are drawn
  // higher the number, less frequently squars are drawn
    // based on modulo
  draw_frame = 10;
  
  depth_side_array = new String[] {"top", "bottom", "left", "right", "top left", "top right", "bottom left", "bottom right"};
}

void draw()
{
  if (frameCount%draw_frame == 0)
  {
    for (int i = 0; i < amount; i++)
    {
      // box color
      grey = random(360);
      //fill(floor(grey));
      
      // box coordinates
      randX1 = random(-side, width + side);
      randY1 = random(-side, height + side);
  
      // randomly select an element from the array
      depth_side = depth_side_array[new Random().nextInt(depth_side_array.length)];
      // boxes
      for (int j = 0; j < depth_boxes; j++)
      {
        // randomly select an element from the array
        //depth_side = depth_side_array[new Random().nextInt(depth_side_array.length)];
      
        switch (depth_side)
        {
          case "top":
            rect(randX1, randY1 + j, side, side);
            break;
          case "bottom":
            rect(randX1, randY1 - j, side, side);
            break;
          case "left":
            rect(randX1 + j, randY1, side, side);
            break;
          case "right":
            rect(randX1 - j, randY1, side, side);
            break;
          case "top left":
            rect(randX1 + j, randY1 + j, side, side);
            break;
          case "top right":
            rect(randX1 - j, randY1 + j, side, side);
            break;
          case "bottom left":
            rect(randX1 + j, randY1 - j, side, side);
            break;
          case "bottom right":
            rect(randX1 - j, randY1 - j, side, side);
            break;
        }
        
      }
    }
  }
}
