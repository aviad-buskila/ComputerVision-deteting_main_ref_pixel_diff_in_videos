from PIL import Image
import image_values


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
