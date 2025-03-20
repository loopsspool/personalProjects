class day_name_box_class
{
  float stroke_weight = DAY_NAME_OUTLINE_WEIGHT;
  float box_width = COL_SIZE;
  float box_height = DAY_NAME_BOX_HEIGHT;
  int buffer_from_gridline_to_usable_space = 1;
  float inside_box_upper_left = stroke_weight/2 + buffer_from_gridline_to_usable_space;
  // 2 * buffer_from_gridline_to_usable_space because once for upper left corner, once for bottom right
  float inner_box_width = box_width - stroke_weight - (2 * buffer_from_gridline_to_usable_space);
  float inner_box_height = box_height - stroke_weight - (2 * buffer_from_gridline_to_usable_space);  
  
  PFont font = body_text_bold;
  int text_size = 14;
  String day_name = "";
  int weekday_num = -1;
  color weekday_color = #FFFFFF;
  
  void display()
  {
    push();
      box();
      day_name_text();
    pop();
  }
  
  void box()
  {
    fill(weekday_color);
    noStroke();
    rect(0, 0, box_width, box_height);

    // Box outline
    // Done this way so "border" doesn't come in on the weekday names because their outline was drawn inside the bordaer
    stroke(0);
    strokeWeight(stroke_weight);
    line(0, 0, box_width, 0);  // Top line
    line(0, box_height, box_width, box_height);  // Bottom line
    if (weekday_num != 0)  // Draws for every cell except the first (so doesn't draw over border)
      line(0, 0, 0, box_height);  // Left line
    if (weekday_num != 6)  // Draws for every cell except the last (so doesn't draw over border)
      line(box_width, 0, box_width, box_height);  // Right line
  }
  
  void day_name_text()
  {
    // Weekday text
    textAlign(CENTER, CENTER);
    textFont(body_text_bold);
    textSize(14);
    fill(0);
    text(day_name, COL_SIZE/2, (DAY_NAME_BOX_HEIGHT/2) - 2); 
  }
  
  void tests()
  {
    // TODO: When the borders get fairly large
      // There's excess room on the left of the first column
      // And the right of the last column
      // This is due to the box expecting there's a thick grid line there
      // When it's been omitted from those
    // Test box to see the interior space of the cell
    //noStroke();
    //fill(360, 100, 100);
    //rect(inside_box_upper_left, inside_box_upper_left, inner_box_width, inner_box_height);
      
    // Test column lines
    //stroke(299, 100, 100);
    //strokeWeight(1);
    //line(0, 0, 0, box_height);
    //line(box_width, 0, box_width, box_height);
    //line(0, 0, box_width, 0);
    //line(0, box_height, box_width, box_height);
  }
}
