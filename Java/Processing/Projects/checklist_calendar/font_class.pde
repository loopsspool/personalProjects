// TODO: check font height of year, see if it matches the month
  // If not, increase until it does

public class font_class
{
  // FONT INFO
  RFont font = default_month_font;
  int size = MONTH_TEXT_SIZE;
  color fill = color(0);
  String text = "default";
  float x = width/2;
  float y = MONTH_BOX_HEIGHT/1.4;
  
  // EFFECTS INFO
  boolean is_outlined = false;
  color outline_color = color(360, 100);
  float outline_weight = 0.2;
  
  boolean is_bolded = false;
  int bold_weight = 2;
  
  boolean is_layered = false;
  boolean layers_are_outlined = false;
  int amount_of_layers = 0;
  int[] layer_colors;
  
  
  void set_features()
  {
    font.setSize(size);
    fill(fill);
    
    if (is_outlined)
    {
      strokeWeight(outline_weight);
      stroke(outline_color);
    }
    else
      noStroke();
    
    translate(x, y);
  }
  
  // TODO: Bring this out of the class or make all the effects part of the class
  void set_layers(int[] layer_colors_)
  {
    amount_of_layers = layer_colors.length;
    layer_colors = layer_colors_;
  }
  
  void display()
  {
    font.draw(text);
  }
}

// TODO: Make this the class display?
void draw_text(font_class Font)
{
  push();
    if (Font.is_bolded)
      bold_font(Font);
    if (Font.is_layered)
      layer_font(Font);
    else
    {
      Font.set_features();
      Font.display();
    }
  pop();
}

// TODO: Make bold font more compatible with other styles
void bold_font(font_class Font)
{
  push();
    Font.set_features();
    // "Bolds" the font a little -- since theres no bold versions of some fonts
    float x_shift_divisor = 5;  // To utilize i as coordinate, small shifts in x
    for (float i = 0; i < Font.bold_weight/x_shift_divisor; i += 1/x_shift_divisor)
    {
      translate(i, 0);
      Font.display();
    }
  pop();
}

// TOFO: Select where the layers show
  // e.g. left to right, diagonally, in a circle, etc
void layer_font(font_class Font)
{
  Font.set_layers(Font.layer_colors);
  if (Font.layers_are_outlined)
  {
    strokeWeight(Font.outline_weight);
    // TODO: add array for outline colors too
    stroke(0);
  }
  else
    noStroke();
    
  float layer_depth = 5;
  float center_layers_adjuster = -(Font.layer_colors.length * layer_depth)/2;
  translate(Font.x + center_layers_adjuster, Font.y + center_layers_adjuster - 5);
  for (int i = 0; i < Font.layer_colors.length; i++)
  {
    fill(Font.layer_colors[i]);
    translate(layer_depth, layer_depth);
    Font.display();
  }
}

/** 
TODO: Text effects: 
  - 3D gradually increasing font size
  - Text Fade in/out
  + See what geomerative can do

**/ 
