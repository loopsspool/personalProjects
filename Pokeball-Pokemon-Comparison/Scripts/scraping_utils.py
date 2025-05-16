import urllib   # For downloading those images to my computer

# NOTE: ALL DOWNLOADS MUST BE DONE IN THE FASHION BELOW
    # Otherwise bulba has a check on if the site is being web scraped and it will block the download
# This is to mask the fact I'm webscraping
    # To use, call
    # filename, headers = opener.retrieve(get_largest_png(img), path + save_name)
opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0')

def download_img(url, save_path):
    filename, headers = opener.retrieve(url, save_path)