from PIL import Image
import image_values


# get the image, and the background RGB value, and count matched and non matched pixels.
# Returns image_values object
def calculate_signal_vs_background(background, image):
    signal_counter = 0
    background_counter = 0
    im = Image.open(image)
    for pixel in im.getdata():
        if pixel == background:
            background_counter += 1
        else:
            signal_counter += 1
    imagevalues = image_values.ImageValues(background_counter, signal_counter)
    return imagevalues
