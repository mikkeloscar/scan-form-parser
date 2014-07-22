#!/usr/bin/python

# Depends
# Pillow (PIL)
# gocr and tesseract
# convert (imagemagic)

from PIL import Image
import sys
import os
import subprocess
import re

def validate_cpr(cpr):
    if len(cpr) != 10:
        return None

    for c in cpr:
        if not c.isdigit():
            return None

    return cpr


def ocr(filename):
    value = subprocess.Popen("gocr -i %s -C '0123456789'" % filename,
                             shell=True,
                             stdout=subprocess.PIPE).stdout.read()
    value = re.sub('[_\n]+', '', value.decode("ascii"))

    return validate_cpr(value)

def tesseract(filename):
    value = subprocess.Popen("./ocr.sh %s" % filename, shell=True,
                             stdout=subprocess.PIPE
                             ).stdout.read().decode("ascii")
    extract = re.search('(\d{6}-\d{4})', value)
    if extract:
        value = re.sub('[-\n]+', '', extract.group(1))

    return validate_cpr(value)


def combine_imgs(img1, img2):
    blank = Image.new("RGB", (580, 320))
    blank.paste(img1, (0, 0))
    blank.paste(img2, (0, 160))
    return blank

def crop(filename, output="billeder"):
    image = Image.open(filename)

    half = False

    # crop ID
    id_box = (1100, 1990, 1680, 2150)
    id_box_half = (1000, 170, 1680, 330)

    cropped_id, id_name = crop_size(image, id_box)

    try:
        cropped_id.save(id_name)
        id_value = tesseract(id_name) or ocr(id_name)

        if not id_value:
            cropped_id_half, id_name = crop_size(image, id_box_half)
            cropped_id_half.save(id_name)
            id_value = tesseract(id_name) or ocr(id_name)
            if not id_value:
                combined = combine_imgs(cropped_id, cropped_id_half)
                combined.show()
                id_value = input("Could not determine CPR\nPlease enter the correct value: ")
            else:
                half = True
        print(id_value)
        print(sys.argv[1])
    except IOError:
        print("ERROR!!")

    # crop ID picture
    img_box = (320, 2400, 736, 2816)
    img_box_half = (300, 570, 716, 986)

    if half:
        cropped_img, name = crop_size(image, img_box_half)
    else:
        cropped_img, name = crop_size(image, img_box)

    # resize ID picture to 200x200
    cropped_img = cropped_img.resize((200, 200))

    # create img dir
    if not os.path.exists(output):
        os.makedirs(output)

    try:
        cropped_img.save(os.path.join(output, "%s.jpg" % id_value))
        # remove tmp file
        os.remove(id_name)
    except IOError:
        print("FAILED")

def crop_size(image, size):
    cropped = image.crop(size)
    name = "tmp-cropped.png"

    return (cropped, name)


def main():
    if len(sys.argv) > 1:
        image_file = sys.argv[1]
    else:
        exit(1)

    if len(sys.argv) > 2:
        crop(image_file, sys.argv[2])
    else:
        crop(image_file)


if __name__ == "__main__":
    main()
