class mountain
{
  float[] point;
  float[][] points;
  
  float x;
  float y;
  float y_off;
  float vertex_y_variation;
  
  mountain(float y_)
  {
    // Figures out how many verticces the mountain will have
      // Keep in mind 3 points are used to make shape cover everything below
          // So starting random number should always be 4 or higher
    int amount_of_vertices = int(random(45, 90));
    // Creates an array to hold the points of each peak
    points = new float[amount_of_vertices][amount_of_vertices];
    
    x = 0;
    y = y_;
    // Noise generation number
    y_off = random(10000);
    
    vertex_y_variation = 300;
  }
  
  void build_mountain()
  {
    // points.length - 3 so can set last points down so shape covers eveything below it
    for (int i = 0; i < points.length - 3; i++)
    {
      // Setting coordinates
      points[i][0] = x;
      // If it is the first point, set the y value to the one given to the constructor
        // This is so the mountains can be started at the top and build downward
      if (i == 0)
        points[0][1] = y;
      else
        points[i][1] = map(noise(y_off), 0, 1, y - vertex_y_variation, y + vertex_y_variation);
      
      // Evenly distributed vertices
        // Minus 4 for the 3 vertices closing the shape and for the first vertex
      x += float(width)/(points.length - 4);  // Float width so the integer division doesn't return an integer, causing the final vertex before closing to fall short
      y_off += .05;
    }
    
    // SETTING END OF SHAPE TO CLOSE ITSELF BELOW ALL VERTICES TO BOTTOM OF WINDOW
    // Lower right corner
    points[points.length - 3][0] = width;
    points[points.length - 3][1] = height;
    // Lower left corner
    points[points.length - 2][0] = 0;
    points[points.length - 2][1] = height;
    // Bringing it back to the first point
    points[points.length - 1][0] = 0;
    points[points.length - 1][1] = points[0][1]; 
  }

  void display()
  {
    beginShape();
    for (int i = 0; i < points.length; i++)
    {
      vertex(points[i][0], points[i][1]);
    }
    endShape();
  }
}
