"""Jpeg to ascii converter"""
from PIL import Image
import structlog
import numpy as np

logger = structlog.get_logger()
greyscale_1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~i!lI;:,\"^\`\". "
greyscale_2 = "@%#*+=-:. "


def get_average(image):
    """Gets the average of the image"""
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w * h))


def convert_jpg_to_ascii(filename, cols, scale, more_levels):
    """Converts a jpg to ascii"""

    image = Image.open(filename).convert("L")
    width, height = image.size
    w = width / cols
    h = w / scale

    rows = int(height / h)

    logger.info("cols and rows", cols=cols, rows=rows)
    logger.info("tile dims", width=w, height=h)
    if cols > width or rows > height:
        logger.error("Image too small for specified cols!")
        exit(0)
    ascii_image = []
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)

        if j == rows - 1:
            y2 = height
        ascii_image.append("")

        for i in range(cols):
            x1 = int(i * w)
            x2 = int((i + 1) * w)

            if i == cols - 1:
                x2 = width

            img = image.crop((x1, y1, x2, y2))
            avg = int(get_average(img))
            if more_levels:
                grayscale_val = greyscale_1[int((avg * 69) / 255)]
            else:
                grayscale_val = greyscale_2[int((avg * 9) / 255)]

            ascii_image[j] += grayscale_val

    return ascii_image


def main():
    """Main function"""
    import argparse
    parser = argparse.ArgumentParser(description="Converts a jpg to ascii")
    parser.add_argument("--file", help="Jpeg file to convert")
    parser.add_argument("--cols", type=int, default=80, help="Number of columns in the output. Default is 80")
    parser.add_argument("--scale", type=float, default=0.43, help="Scale of the output. Default is 0.43")
    parser.add_argument("--more_levels", action="store_true", help="Use more levels of grayscale")
    args = parser.parse_args()
    logger.info("args", args=args)
    ascii_image = convert_jpg_to_ascii(args.file, args.cols, args.scale, args.more_levels)

    with open("ascii.txt", "w") as f:
        for row in ascii_image:
            f.write(row + "\n")


if __name__ == "__main__":
    main()
