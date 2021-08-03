import pytesseract
from PIL import Image


def clear_image(image):
    image = image.convert('RGB')
    width = image.size[0]
    height = image.size[1]

    for x in range(width):
        for y in range(height):
            rgb = image.getpixel((x, y))
            if rgb[0] >= 140 and rgb[1] >= 140 and rgb[2] >= 140:
                image.putpixel((x, y), (0, 0, 0))
            else:
                image.putpixel((x, y), (255, 255, 255))
    return image


def get_code(img_path):
    image = Image.open(img_path)
    image = clear_image(image)
    code = pytesseract.image_to_string(image, lang='eng', config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
    return "".join(code.split())


if __name__ == '__main__':
    print(get_code('../1.jpg'))
