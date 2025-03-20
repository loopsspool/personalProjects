// Used to evaluate time between born date and today
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

String BORN_DATE;
int EXPECTED_YEARS;  // Expectancy to base years, weeks, and days expectancy
HashMap<String, Integer> EXPECTED;  // Life expectancy in years, weeks, and days
int LIVED_DAYS;  // How long you've lived in days
HashMap<String, Integer> LIVED;  // Maps days lived to weeks and years
int ADULT_START_AGE;  // What age you consider yourself an adult
int ADULT_DAYS;
HashMap<String, Integer> ADULT_LIVED;
int KID_END_AGE;  // What age you consider your childhood over
int KID_DAYS;  // Amount of days lived as kid
HashMap<String, Integer> KID_LIVED;

// TODO: Add in text of remaining <selected_interval>
int REMAINING;
String SELECTED_INTERVAL;  // How grid shows up (days, weeks, months, years)

int SCALE;  // Size of squares based off window width & height
int COLS, ROWS;
int CURRENT_SQUARE;  // Tracks square count

void setup()
{
  // TODO: Make it easier to change window size and have grids adapt (some split)
  size(800, 800);
  // Makes it so when sketch pops up doesn't interfere with code window
  surface.setLocation(70, 100);
  colorMode(HSB, 360, 100, 100);
  
  BORN_DATE = "1998-10-24";
  KID_END_AGE = 12;
  ADULT_START_AGE = 18;
  EXPECTED_YEARS = 80;
  SELECTED_INTERVAL = "YEARS";
  
  // TODO: Format the string so you can write dates how you're used to
  // 0 is for the add_years parameter, in this case is none
  LIVED_DAYS = days_between_to_current(BORN_DATE, 0);
  // TODO: Color in half squares (using rect) for weeks/months/years unfinished
  LIVED = new HashMap<String, Integer>();
  LIVED.put("DAYS", LIVED_DAYS);
  LIVED.put("WEEKS", LIVED_DAYS / 7);
  LIVED.put("MONTHS", LIVED_DAYS / 30);
  LIVED.put("YEARS", LIVED_DAYS / 365);
  
  
  EXPECTED = new HashMap<String, Integer>();
  EXPECTED.put("YEARS", EXPECTED_YEARS);
  EXPECTED.put("MONTHS", EXPECTED_YEARS * 12);
  EXPECTED.put("WEEKS", EXPECTED_YEARS * 52);
  EXPECTED.put("DAYS", EXPECTED_YEARS * 365);
  
  
  ADULT_DAYS = days_between_to_current(BORN_DATE, ADULT_START_AGE);
  ADULT_LIVED = new HashMap<String, Integer>();
  //////////////////////  CAREFUL!!!  //////////////////////
    // This IS NOT a count of adult times lived!!!!
    // This IS the square count above where adult times are
      // TODO: Consider changing in the future?
  ADULT_LIVED.put("DAYS", LIVED.get("DAYS") - ADULT_DAYS);
  ADULT_LIVED.put("WEEKS", LIVED.get("WEEKS") - (ADULT_DAYS / 7));
  ADULT_LIVED.put("MONTHS", LIVED.get("MONTHS") - (ADULT_DAYS / 30));
  ADULT_LIVED.put("YEARS", LIVED.get("YEARS") - (ADULT_DAYS / 365));
  
  
  KID_DAYS = days_between_two_dates(BORN_DATE, KID_END_AGE);
  KID_LIVED = new HashMap<String, Integer>();
  KID_LIVED.put("DAYS", KID_DAYS);
  KID_LIVED.put("WEEKS", KID_DAYS / 7);
  KID_LIVED.put("MONTHS", KID_DAYS / 30);
  KID_LIVED.put("YEARS", KID_DAYS / 365);
  
  
  
  CURRENT_SQUARE = 0;
  // Finds next perfect square for grid size
    // Consequence of this is the grid will always attempt to be as square as possible
      // So sometimes doesn't fill screen nicely (ie selected interval of days)
  int grid_size = floor(sqrt(EXPECTED.get(SELECTED_INTERVAL))) + 1;
  COLS = grid_size;
  ROWS = grid_size;
  SCALE = width / COLS;

  background(0);
  stroke(0);
  //noStroke();
  
  // Label used to break outer loop from inner loop
  outer_loop:
  for (int y = 0; y < ROWS; y++)
  {
    for (int x = 0; x < COLS; x++)
    {
      // Tracks squares made so grid doesn't exceed expectancy
      CURRENT_SQUARE++;
      if (CURRENT_SQUARE > EXPECTED.get(SELECTED_INTERVAL))
        break outer_loop;
      
      // If square is a lived day, shade
      if (CURRENT_SQUARE <= LIVED.get(SELECTED_INTERVAL))
      {
        // Teen years shaded yellow
        fill(62, 100, 100);
        // If square is a KID lived day, shade red
        if (CURRENT_SQUARE <= KID_LIVED.get(SELECTED_INTERVAL))
          fill(0, 100, 100);
        // If square is an ADULT lived day, shade green
        if (CURRENT_SQUARE >= ADULT_LIVED.get(SELECTED_INTERVAL))
          fill(110, 100, 100);
      }
      // If square not lived yet, shade very light grey
      else
        fill(350);
      
      square(x * SCALE, y * SCALE, SCALE);
    }
  }
}

int days_between_to_current(String start_string, int add_years)
{
  // Parses date string into a LocalDate object to be compared w current date
  LocalDate start_date = LocalDate.parse(start_string);
  // Adding years if needed
  start_date = start_date.plusYears(add_years);
  // Gets current date
  LocalDate current_date = LocalDate.now();
  // Figures out time between start date and today
  return int(ChronoUnit.DAYS.between(start_date, current_date));
}

int days_between_two_dates(String start_string, int add_years_for_end)
{
  // Parses date string into a LocalDate object to be compared w current date
  LocalDate start_date = LocalDate.parse(start_string);
  // Adding years
  LocalDate end_date = start_date.plusYears(add_years_for_end);
  // Figures out amount of days in between the two dates
  return int(ChronoUnit.DAYS.between(start_date, end_date));
}
