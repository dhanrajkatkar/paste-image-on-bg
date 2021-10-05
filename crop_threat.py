import cv2
from os import path, scandir

ref_point = []


def crop_threat_image(image):
    #     image = cv2.imread(image_path)
    clone = image.copy()
    cv2.namedWindow("image")
    p = cv2.setMouseCallback("image", shape_selection)

    # keep looping until the 'q' key is pressed
    while True:
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # press 'r' to reset the window
        if key == ord("r"):
            image = clone.copy()

        # press 'q' to quit the cropping
        elif key == ord("q"):
            break

        # press 's' to save cropped threat image
        elif key == ord("s"):
            if not path.exists('cropped/cropped.png'):
                cv2.imwrite('cropped/cropped.png',
                            clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]])
            else:
                counter = 0
                filename = f'cropped/cropped{counter}.png'
                while path.exists(filename):
                    counter += 1
                    filename = f'cropped/cropped{counter}.png'
                    print('.')
                cv2.imwrite(filename, clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]:ref_point[1][0]])

    # close all open windows
    cv2.destroyAllWindows()


def shape_selection(event, x, y, flags, param):
    # grab references to the global variables
    global ref_point, image

    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being performed
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_point = [(x, y)]

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        ref_point.append((x, y))
        print(ref_point)
        # draw a rectangle around the region of interest
        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)
        cv2.imshow("image", image)


if __name__ == '__main__':
    # path to output cropped folder
    cropped_path = 'cropped'
    # path to threat folder
    threat_images_path = 'threat_images'

    counter = 0
    for threat_image in scandir(threat_images_path):
        output_filename = path.join(cropped_path, f'{counter}.png')
        image = cv2.imread(threat_image.path)
        crop_threat_image(image)
        counter += 1
