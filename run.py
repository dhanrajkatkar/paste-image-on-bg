from PIL import Image, ImageFilter, ImageEnhance
from random import randint
from os import path, scandir
from tqdm import tqdm


def remove_bg(img):
    pixel_filter = (200, 200, 200)
    colour_correction_ratios = (.9, 1, 1)
    threat_transparency_factor = .9
    thread_brightness_factor = .6

    #     img = Image.open('fg.png')
    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[0] > pixel_filter[0] and item[1] > pixel_filter[1] and item[2] > pixel_filter[2]:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append((max(round(item[0] * colour_correction_ratios[0]), 0),
                             max(round(item[1] * colour_correction_ratios[1]), 0),
                             max(round(item[2] * colour_correction_ratios[2]), 0),
                             round(item[3] * threat_transparency_factor)))

    img.putdata(new_data)

    img = img.filter(ImageFilter.SMOOTH)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(thread_brightness_factor)
    return img


def paste_on_bg(threat_path, bg_path, output_filename='output.png'):
    # counter clockwise
    rotation_angle = 45
    threat_image_path = threat_path
    background_image_path = bg_path
    background_transparency_factor = 1

    # Open Front Image
    front_image = Image.open(threat_image_path)
    front_width = front_image.width
    front_height = front_image.height
    front_image = remove_bg(front_image)

    # Open Background Image
    background = Image.open(background_image_path)
    background_width = background.width
    background_height = background.height

    # to make sure threat does not go out of the ROI
    threat_paste_coords = (randint(round(background_width * .15), round(background_width * .6)),
                           randint(round(background_height * .15), round(background_height * .6)))

    # Convert image to RGBA
    front_image = front_image.convert("RGBA")
    front_image = front_image.rotate(rotation_angle, Image.NEAREST, expand=1)

    # adaptive scaling factor for different size of images
    threat_scale_factor = randint(round(max(front_width, front_height, background_width, background_height) * .25),
                                  round(max(front_width, front_height, background_width, background_height) * .5)) / max(
        front_width, front_height)

    front_image = front_image.resize(
        (round(front_width * threat_scale_factor), round(front_height * threat_scale_factor)))

    # Convert image to RGBA
    background = background.convert("RGBA")

    # making bg transparent
    if background_transparency_factor != 1:
        datas = background.getdata()
        new_data = []
        for item in datas:
            new_data.append((item[0], item[1], round(item[2]), round(item[3] * background_transparency_factor)))
        background.putdata(new_data)

    # Paste the front_image at (width, height)
    background.paste(front_image, threat_paste_coords, front_image)

    # Save this image
    background.save(output_filename, format="png")


if __name__ == '__main__':
    # path to cropped threat folder
    cropped_path = 'cropped'
    # path to background folder
    bg_path = 'background_images'
    # path to output folder
    output_path = 'output'
    counter = 0
    for threat_image in tqdm(scandir(cropped_path)):
        for bg_image in scandir(bg_path):
            output_filename = path.join(output_path, f'{counter}.png')
            paste_on_bg(threat_image.path, bg_image.path, output_filename)
            counter += 1
