from PIL import Image, ImageChops   # For downloading image, cropping, and border checking
import os   # For file moving and checking

# Helper function for is_there_a_border
def find_solid_border_corner(im):
    im = im.convert('RGBA')
    # Checking each corners alpha values
        # Sometimes there's a thin line of transparency
            # Without this, that's interpreted as a "border"
    # Checking top left corner alpha
    if im.getpixel((0, 0))[3] != 0:
        return ((0, 0))
    # Checking top right corner alpha
    if im.getpixel((im.width-1, 0))[3] != 0:
        return ((im.width-1, 0))
    # Checking bottom right corner alpha
    if im.getpixel((im.width-1, im.height-1))[3] != 0:
        return ((im.width-1, im.height-1))
    # Checking bottom left corner alpha
    if im.getpixel((0, im.height-1))[3] != 0:
        return ((0, im.height-1))

    # If all corners are transparent, return -1
    return (-1)

# Checks to see if there's an image around a border
# Courtesy of https://stackoverflow.com/questions/10985550/detect-if-an-image-has-a-border-programmatically-return-boolean
def there_is_a_border(img_name):
    im = Image.open(img_name)
    solid_color_reference_corner = find_solid_border_corner(im)
    # If all four corners are transparent, exit function
    if solid_color_reference_corner == -1:
        return (False)
    
    bg = Image.new(im.mode, im.size, im.getpixel(solid_color_reference_corner))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    # If image has border on any side, print filename
    if bbox != (0,0,im.size[0],im.size[1]):
        return (True)

def remove_border(img_name):
    im = Image.open(img_name)
    solid_color_reference_corner = find_solid_border_corner(im)
    # If all four corners are transparent, exit function
    if solid_color_reference_corner == -1:
        return (False)

    bg = Image.new(im.mode, im.size, im.getpixel(solid_color_reference_corner))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        im = im.crop(bbox)
        im.save(img_name)

# NOTE: Change this path based on the files you'd like to change
img_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon\\Game Sprites\\initial_downloads_for_border_removal\\"
img_files = os.listdir(img_path)

for img in img_files:
    # Skipping over the directory to send borderless images to
    if img == "no borders":
        continue
    if there_is_a_border(img_path + img):
        print(img)