public class daily_box_class
{
  float stroke_weight = DAY_GRID_STROKE_WEIGHT;

  float box_width = COL_SIZE;
  float box_height = ROW_SIZE;
  int buffer_from_gridline_to_usable_space = 1;
  float inside_box_upper_left = stroke_weight/2 + buffer_from_gridline_to_usable_space;
  // 2 * buffer_from_gridline_to_usable_space because once for upper left corner, once for bottom right
  float inner_box_width = box_width - stroke_weight - (2 * buffer_from_gridline_to_usable_space);
  float inner_box_height = box_height - stroke_weight - (2 * buffer_from_gridline_to_usable_space);
  
  int day_number = -1;
  int col_number = -1;
  String[] check_off_items = {"Do morning routine", 
                              "Be present", 
                              "Do thing you love", 
                              "Spend time w/ self", 
                              "Do list"};
  color day_color = #FFFFFF;
  boolean in_month = false;

  void display()
  {
    push();   
      box();
    pop();
  }
  
  void box()
  {
    noStroke();

      // Grey out days not in month
      if (day_number == 0 || day_number > DAYS_IN_MONTH)
      {
        // If day color is default white, make out of month boxes grey
        if (day_color == #FFFFFF)
          fill(280);
        // But if the values been changed, shade them that color
        else
          fill(day_color);
        rect(0, 0, box_width, box_height);
      }
      else
      {
        fill(day_color);
        rect(0, 0, box_width, box_height);
        
        numbers();
        checklist();
        done_today_checkbox();
      }
      
      // Box outline
      stroke(0);
      strokeWeight(stroke_weight);
      line(0, 0, box_width, 0);  // Top line
      line(0, box_height, box_width, box_height);  // Bottom line
      if (col_number != 0)  // Draws for every cell except the first (so doesn't draw over border)
        line(0, 0, 0, box_height);  // Left line
      if (col_number != 6)  // Draws for every cell except the last (so doesn't draw over border)
        line(box_width, 0, box_width, box_height);  // Right line
  }
  
  void numbers()
  {
    push();
      translate(4, 8);
      textAlign(LEFT, CENTER);
      textFont(body_text_bold);
      textSize(12);
      stroke(0);
      fill(0);
      text(String.valueOf(day_number), 0, 0);
    pop();
  }
  
  void checklist()
  {
    float indent = 13;
    float size = 9.4;
    float y_translate = 0;
    // Adjusting for rows of calendar so alignment doesn't look funky
    // TODO: Align to liking
    if (AMOUNT_OF_ROWS == 6)
      y_translate = 11.7;
    if (AMOUNT_OF_ROWS == 5)
      y_translate = 14.5;
    if (AMOUNT_OF_ROWS == 4)
      y_translate = 18;
    
    push();
      textFont(body_text);
      
      translate(7, 7);
      for (int i = 0; i < check_off_items.length; i++)
      {
        translate(0, y_translate);
        noFill();
        strokeWeight(1);
        stroke(0);
        square(0, 0, size);
        textSize(size);
        textAlign(LEFT);
        fill(0);
        text(check_off_items[i], indent, 0.9 * size);
      }
    pop();
  }
  
  void done_today_checkbox()
  {
    push();
      rectMode(CENTER);
      noFill();
      strokeWeight(1);
      stroke(0);
      // Matches checkbox items square size
      float square_size = 9.4;
      // -1 on x and +8 on y to align with day numbers
      square(box_width - square_size - 1, square_size/4 + 8, square_size);
    pop();
  }
}

void tests()
{
      // TODO: When the borders get fairly large
        // There's excess room on the left of the first column
        // And the right of the last column
        // This is due to the box expecting there's a thick grid line there
        // When it's been omitted from those
      // INSIDE BOX TEST
      //noStroke();
      //fill(360, 100, 100);
      //rect(inside_box_upper_left, inside_box_upper_left, inner_box_width, inner_box_height);
    
}
