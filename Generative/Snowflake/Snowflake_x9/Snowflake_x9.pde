import java.util.ArrayList;

int GRID_ROWS = 30;
int GRID_COLS = 30;
int GRID_PRODUCT = GRID_ROWS * GRID_COLS;
Snowflake[] snowflakes = new Snowflake[GRID_PRODUCT];

// Padding around individual snowflakes
int SNOWFLAKE_PADDING = 5;
int SNOWFLAKE_PADDING_BOTH_SIDES = SNOWFLAKE_PADDING * 2;
// Window border padding
int WINDOW_PADDING = 10;
int WINDOW_PADDING_BOTH_SIDES = WINDOW_PADDING * 2;

void settings()
{
  // Setting ssketch window to left side of screen
  // -70 accounts for navigation bar
  size(int(displayWidth/2), int(displayHeight - 70));
}

void setup()
{
  surface.setLocation(0, 0);
  
  // Dividing window for spacing of snowflakes
  float x_spacing = (width - WINDOW_PADDING_BOTH_SIDES)/GRID_COLS;
  float y_spacing = (height - WINDOW_PADDING_BOTH_SIDES)/GRID_ROWS;
  
  // Dividing by 2 to get radius, not diameter
  float xr, yr;
  float useable_grid_r = 0;
  xr = (x_spacing - SNOWFLAKE_PADDING_BOTH_SIDES)/2;
  yr = (y_spacing - SNOWFLAKE_PADDING_BOTH_SIDES)/2;
  // Getting smallest radius that'll fit in grid square
    // The bigger the amount of rows/cols, the smaller the radius
      // So smaller radius must be used to ensure fit
  if (xr <= yr)
    useable_grid_r = xr;
  else
    useable_grid_r = yr;
    
  // Initializing snowflakes array 
  int row_acc = 0;
  int col_acc = 0;
  for (int i = 0; i < snowflakes.length; i++)
  {
    // Initializing snowflakes
    float x = (col_acc * x_spacing) + xr + SNOWFLAKE_PADDING + WINDOW_PADDING;
    float y = (row_acc * y_spacing) + yr + SNOWFLAKE_PADDING + WINDOW_PADDING;

    //Identifying information is +1 so my visual-based brain doesn't have to do programming math lol
    snowflakes[i] = new Snowflake(x, y, useable_grid_r, i + 1, row_acc + 1, col_acc + 1);
    
    col_acc += 1;
    // If end of column reached, reset and add to row count
    if (col_acc%GRID_COLS == 0)
    {
      col_acc = 0;
      row_acc += 1;
    }
  }
  noLoop();
}

void draw()
{
  fill(255, 0, 0);
  line(width, 0, width, height);
  for(int i=0; i<snowflakes.length; i++)
    snowflakes[i].display();
}

class Snowflake 
{
  // FUNDAMENTALS
  int number, row, col;  // Identifying information
  float ox, oy;  // Centered origin points
  float or; // Radius of display grid for an individual snowflake, based off of # of rows/cols & padding
  // ARMS
  float starting_arm_angle = radians(random(0, 360));
  int amount_of_arms = floor(random(3, 16)); // Longest extensions from center
  boolean arms_are_equally_spaced = boolean(floor(random(2)));
  int amount_of_groups = 0;
  int arms_per_group = 1;  // Amount of arms within an unevenly spaced "group"
  float group_spacing = radians(random(.25 * (360/amount_of_arms), 330));
  //boolean has_multiple_group_sizes = boolean(floor(random(2)));
  //float[] arm_length = new float[amount_of_arms];
  float arm_length = 0;
  //boolean arms_are_equal_length = boolean(floor(random(2)));
  Snowflake(float x, float y, float r, int num, int ro, int co)
  {
    ox = x;
    oy = y;
    or = r;
    arm_length = or;
    
    number = num;
    row = ro;
    col = co;
    
    check_dependent_variables();
    print_diagnostics();
  }
  
  void display()
  {
    push();
      translate(ox, oy);
      rotate(starting_arm_angle);
      for (int i=0; i<amount_of_arms; i++)
      { 
        if (arms_are_equally_spaced)
        {
          rotate(radians(360/amount_of_arms));
          line(0, 0, 0, arm_length);
        }
        else
        {
          // Rotation for each group
          rotate(radians(360/(amount_of_arms/arms_per_group)));
          // Rotation for each arm in group
          push();
            for (int i_ = 0; i_ < arms_per_group; i_++)
            {
              rotate(group_spacing);
              line(0, 0, 0, arm_length);
            }
          pop();
        }
      }
    pop();
  }
  
  void check_dependent_variables()
  {
    // For snowflakes with less arms, prevent them from being spaced unequally
    if (amount_of_arms < 6 && !arms_are_equally_spaced)
    {
      arms_are_equally_spaced = true;
      return;
    }
    // Denominators of amount of arms
    ArrayList<Integer> denoms = new ArrayList<Integer>();
    // Getting group size
    if (!arms_are_equally_spaced)
    {
      // Checking for denominators
        // NOTE: Skips 1
      for (int i=2; i<=amount_of_arms; i++)
      {
        if (amount_of_arms%i == 0 && i != amount_of_arms)
          denoms.add(i);
      }
      // If only denominator is the number of arms itself (prime), do not group
      if (denoms.size() == 0)
      {
        arms_are_equally_spaced = true;
        return;
      }
      // Calculating amount of groups of arms
      int random_el;
      boolean only_two_groups = true;
      // If there's less than two groups, find a different amount of groups
        //Snowflakes with less arms look weird in two group forms
          //There is an exception for snowflakes with more arms because they fan out wider
      while (only_two_groups)
      {
        random_el = int(random(denoms.size()));
        arms_per_group = denoms.get(random_el);
        amount_of_groups = amount_of_arms/arms_per_group;
        // If only 2 groups of arms in a 6-armed or less snowflake, re-analyze
        if (amount_of_groups == 2 && amount_of_arms <= 6)
          continue;
        else
          only_two_groups = false;
      }
    }
  }
  
  void print_diagnostics()
  {
    print("\n #", number, "     row: ", row, "     col:", col);
    print("\n", amount_of_arms, " arms that are evenly spaced: ", arms_are_equally_spaced);
    print("\n", arms_per_group, " arms in ", amount_of_groups, " groups rotated ", degrees(group_spacing), " degrees each");
    print("\n\n");
  }
  
}
