import java.util.*;  // For Date
import java.time.*;  // For LocalDate
import processing.pdf.*;  // To convert to PDF
import geomerative.*;  // For text outline

// PDF Switcher
boolean is_PDF = false;
// TODO: See if you can automatically open the pdf after playing

// GENERAL DATE STUFF
String[] WEEKDAYS = {"MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"};

// CURENT DATE STUFF
Date CURRENT_DATE;
LocalDate LOCAL_DATE;
int YEAR, MONTH, DAY;
String DAY_NAME;
String MONTH_NAME;
String MONTH_AND_YEAR;
String FIRST_DAY_OF_MONTH_NAME;
int FIRST_DAY_OF_MONTH_COLUMN;
int DAYS_IN_MONTH;

// CALENDAR ALIGNMENTS
float MONTH_BOX_HEIGHT;
float DAY_NAME_BOX_HEIGHT = 25;

// CALENDAR GRID INFO
int AMOUNT_OF_ROWS;
float ROW_SIZE;
float COL_SIZE;
/** Here's the thing....
  A proper calendar has to have column lines that match up
  The day name lines have to continue down to the day grid lines
  They can be different sizes, but they have to be centered along the same point
  
  I wanted this calendar also to have a border around it
  And no matter how thick the day grid or day name strokes were, the border would always take precedence
  In other words there would be a straight border line from the month art, down through the day names and day grid
    For example, if the day name and day grid strokeWeight were set at 20, but the calendar border were set at 1
      The calendar would have a 1 pixel wide border all around
      Even though the internal lines for the grid and names boxes would be pretty chonky
  
  To have both of the above criteria
  I would have to adjust day grid or day name cell widths based off of their strokeWeight to hide the stroke in the border
  But then text wouldn't be centered correctly
  And the strokes were overlapping, appearing thicker than they should because the cells were wider than COL_SIZE but being x-translated by that variable
  So I'd have to adjust the x-translate based off of the width adjustments
  If I were to do that the columns would no longer adhere to the necessary continuously uniform column widths from day names to day grid
  
  So I had two options:
    1) Require day name strokeWeight to be the same as day grid strokeWeight
    2) "Fake" the strokeWeight by drawing lines over the original strokes, with the exceptions of the ones "covered" by the calendar border
    
  I opted for the latter option since I wanted complete freedom for this calendar
  If I wanted day name strokeWeight 10x that of the day grid strokeWeight I wanted to be able to do that
  
  So do note when altering the below variables
  As it appears you are altering direct strokeWeight of their rectangles
  You are not
  
  This complicates things inside their respective class display functions a bit
  But greatly simplifies their size and translate calls
  
  Phew... This was a PITA to figure out but I'm glad I did
  I don't like hinky dink workarounds or "faking" code like this
  But unfortunately in this case I believe it is necessary
**/
float DAY_GRID_STROKE_WEIGHT = 1;  
float CALENDAR_BORDER_WEIGHT = 4;
float CALENDAR_BORDER_BUFFER = CALENDAR_BORDER_WEIGHT/2;  // So strokeWeight lines up with pixels inside border to align all squares the same
float DAY_NAME_OUTLINE_WEIGHT = 2;
float DAY_NAME_OUTLINE_BUFFER = DAY_NAME_OUTLINE_WEIGHT/2;
daily_box_class[] day_boxes;
day_name_box_class[] day_names;

// FONTS
int MONTH_TEXT_SIZE = 60;
RFont default_month_font;
PFont month_font;
PFont body_text;
PFont body_text_bold;

// GRAPHICS
PGraphics month_banner;


void settings()
{
  // TODO: Test if the below is even true
  //////////////////////////////    WARNING    //////////////////////////////
  // Sizes pretty much have to remain here for rows/cols to display evenly
    // height 600 is divisible by 4, 5, and 6 (all possible row amounts) so will always have rounded int row lines
  
  if (is_PDF)
  {
    size(780, 600, PDF, "calendar_test.pdf");
  }
  else
  {
    size(780, 600);
    noLoop();
  }
}

void setup()
{
  surface.setLocation(50, 50);
  colorMode(HSB, 360, 100, 100, 100);
  textAlign(CENTER, CENTER);
  strokeCap(SQUARE);
  background(360);
  
  // Uncomment to view available fonts
  //String[] fontList = PFont.list();
  //printArray(fontList);
  RG.init(this);  // Initializes geomerative stuff
  default_month_font = new RFont("data\\CASTELAR.TTF", 60, RFont.CENTER);
  month_font = createFont("Castellar", 60);
  body_text = createFont("Century Schoolbook", 12);
  body_text_bold = createFont("Century Schoolbook Bold", 12);
  
  // CALENDAR ALIGNMENT
  // TODO: See if the below is needed
  //////////////////////////////    WARNING    //////////////////////////////
  // -7 here to keep (MONTH_BOX_HEIGHT + DAY_NAME_BOX_HEIGHT + DAY_NAME_OUTLINE_BUFFER + CALENDAR_BORDER_BUFFER) == 120
    // 120 is a multiple of 60 (divisible by 4, 5, and 6 (all possible row amounts))
      // So rows will always fall on rounded integers
  // If adjusting ANY of the variables above, adjust this so the sum will == 120
  MONTH_BOX_HEIGHT = height/6 - 7;
    // TODO: Adjust with border weight
  
  // DATE STUFF
  CURRENT_DATE = new Date();
  LOCAL_DATE = CURRENT_DATE.toInstant().atZone(ZoneId.systemDefault()).toLocalDate();
  LOCAL_DATE = LOCAL_DATE.plusMonths(1);
  YEAR = LOCAL_DATE.getYear();
  MONTH = LOCAL_DATE.getMonthValue();
  DAY = LOCAL_DATE.getDayOfMonth();
  MONTH_NAME = LOCAL_DATE.getMonth().toString();
  FIRST_DAY_OF_MONTH_NAME = LOCAL_DATE.minusDays(DAY-1).getDayOfWeek().toString();
  MONTH_AND_YEAR = MONTH_NAME + " " + YEAR;
  DAYS_IN_MONTH = LOCAL_DATE.lengthOfMonth();
  
  // GRID STUFF
  AMOUNT_OF_ROWS = 5;
  
  // Finding what column month starts in
  FIRST_DAY_OF_MONTH_COLUMN = 0;
  while (WEEKDAYS[FIRST_DAY_OF_MONTH_COLUMN] != FIRST_DAY_OF_MONTH_NAME)
    FIRST_DAY_OF_MONTH_COLUMN++;
  
  // Adding a row if days don't fit into 7x5 grid
    // If longer month starts later in the week
  int DAYS_FITTING_INTO_7X5 = 35 - FIRST_DAY_OF_MONTH_COLUMN;
  if (DAYS_FITTING_INTO_7X5 < DAYS_IN_MONTH)
    AMOUNT_OF_ROWS = 6;
  
  // If February starts on a Monday and it isn't a leap year it only needs 4 rows
  if ((DAYS_IN_MONTH == 28) && (FIRST_DAY_OF_MONTH_COLUMN == 0))
    AMOUNT_OF_ROWS = 4;

  // CALENDAR_BORDER_WEIGHT - 0.5 to hide the default strokeWeight of 1 within the bottom border
    // Also allows cell heights to be ROW_SIZE, not that +/- something
  ROW_SIZE = height - (MONTH_BOX_HEIGHT + DAY_NAME_BOX_HEIGHT + DAY_NAME_OUTLINE_BUFFER + CALENDAR_BORDER_WEIGHT - 0.5);
  ROW_SIZE /= AMOUNT_OF_ROWS;
  
  // CALENDAR_BORDER_WEIGHT - 0.5 to hide the default strokeWeight of 1 within the border
    // Also allows cell widths to be COL_SIZE, not that +/- something
  COL_SIZE = (float(width) - (2 * (CALENDAR_BORDER_WEIGHT - 0.5)))/7;
  
  // Initializing daily squares
  int square_amount = AMOUNT_OF_ROWS * 7;
  day_boxes = new daily_box_class[square_amount];
  for (int i = 0; i < square_amount; i++)
  {
    day_boxes[i] = new daily_box_class();
    
    // Setting their in_month property
    // + FIRST_DAY_OF_MONTH_COLUMN because i is tracking box number, which will include initial greyed out boxes, so offset the end of the month check by that amount
    if (i >= FIRST_DAY_OF_MONTH_COLUMN && i < (DAYS_IN_MONTH + FIRST_DAY_OF_MONTH_COLUMN))
      day_boxes[i].in_month = true;
    else
      day_boxes[i].in_month = false;
  }
    
  // Initializing weekday rectangles
  day_names = new day_name_box_class[7];
  for (int i = 0; i < 7; i++)
  {
    day_names[i] = new day_name_box_class();
    day_names[i].day_name = WEEKDAYS[i];
    day_names[i].weekday_num = i;
  }
}

void draw()
{
  month_art();
  month_art_cutoff();
  draw_daily_boxes();
  weekday_names();
  calendar_outline();
    
  if (is_PDF)
    exit();
}

void month_art_cutoff()
{
  // White box covering any overlap from the monthly art header
  push();
    noStroke();
    fill(360);
    rect(0, MONTH_BOX_HEIGHT, width, height);
  pop();
}

// TODO: Maybe put this function and the weekday names list inside of the class?
  // Same with daily boxes
void weekday_names()
{
  push();
    translate(CALENDAR_BORDER_WEIGHT - 0.5, MONTH_BOX_HEIGHT);
    for (int i = 0; i < 7; i++)
    {
      day_names[i].display();
      translate(COL_SIZE, 0);
    }
  pop();
}

void draw_daily_boxes()
{
  int square_acc = 0;
  int day_acc = 0;
  int col_acc = 0;
  
  // If month starts on a Monday (first square), make it day 1
      // So square doesn't get greyed out & day number shows as 1
        // Since normally isn't accumulated until after function calls
  if (FIRST_DAY_OF_MONTH_COLUMN == 0)
    day_acc++;
    
  push();
    // NOTE: Factor in that a rect with stroke will apply ONLY half the stroke in the upper left hand corner
      // Hence the stroke_weight adjuster at the end of the x & y translate
    translate(CALENDAR_BORDER_WEIGHT - 0.5, MONTH_BOX_HEIGHT + DAY_NAME_BOX_HEIGHT + DAY_NAME_OUTLINE_BUFFER);

    for (int y = 0; y < AMOUNT_OF_ROWS; y++)
    {
      for (int x = 0; x < 7; x++)
      {
        day_boxes[square_acc].col_number = col_acc;
        day_boxes[square_acc].day_number = day_acc;
        day_boxes[square_acc].display();
        
        // Moving onto next day
        col_acc++;
        square_acc++;
        if (square_acc >= FIRST_DAY_OF_MONTH_COLUMN)
          day_acc++;
          
        translate(COL_SIZE, 0);
      }
      // Moving onto next week
      col_acc = 0;
      translate(-(COL_SIZE * 7), ROW_SIZE);
    }
  pop();
}

void calendar_outline()
{
  push();
    stroke(0);
    strokeWeight(CALENDAR_BORDER_WEIGHT);
    line(CALENDAR_BORDER_BUFFER, 0, CALENDAR_BORDER_BUFFER, height);  // LEFT
    line(width - CALENDAR_BORDER_BUFFER, 0, width - CALENDAR_BORDER_BUFFER, height);  // RIGHT
    line(0, CALENDAR_BORDER_BUFFER, width, CALENDAR_BORDER_BUFFER);  // TOP
    line(0, height - CALENDAR_BORDER_BUFFER, width, height - CALENDAR_BORDER_BUFFER);  // BOTTOM
  pop();
}
