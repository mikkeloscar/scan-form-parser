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

def crop(filename, output="billeder"):
    image = Image.open(filename)

    # crop ID
    id_box = (1100, 1990, 1680, 2150)
    cropped_id = image.crop(id_box)

    id_name = "tmp-id.png"

    try:
        cropped_id.save(id_name)
        # id_value = ocr(id_name)
        id_value = tesseract(id_name) or ocr(id_name)

        if not id_value:
            cropped_id.show()
            id_value = input("Could not determine CPR\nPlease enter the correct value: ")
        print(id_value)
    except IOError:
        print("ERROR!!")

    # crop ID picture
    img_box = (320, 2400, 736, 2816)
    cropped_img = image.crop(img_box)
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
