from pathlib import Path
from PIL import Image
from sys import argv


CHAR_WIDTH = 12
CHAR_HEIGHT = 18

CHAR_COUNT_X = 16
CHAR_COUNT_Y = 16

SRC_SCALE_FACTOR = 1
DST_SCALE_FACTOR = 3

CHAR_WIDTH_PX = CHAR_WIDTH * SRC_SCALE_FACTOR
CHAR_HEIGHT_PX = CHAR_HEIGHT * SRC_SCALE_FACTOR

DST_PAGES = 2
DST_CHAR_COUNT = CHAR_COUNT_X * CHAR_COUNT_Y * DST_PAGES

# INav font PNGs have a black outline around the entire image. Betaflight
# doesn't!?
WITH_INITIAL_INDENT = False


def main():
    src_img_path = Path(argv[1])
    src_img = Image.open(src_img_path)
    src_pages = int(src_img.height / CHAR_HEIGHT_PX / CHAR_COUNT_Y)

    dst_img = Image.new(
        "RGBA",
        (
            CHAR_WIDTH_PX * CHAR_COUNT_X,
            CHAR_HEIGHT_PX * CHAR_COUNT_Y * DST_PAGES,
        ),
        (0, 0, 0, 0),
    )

    for j in range(0, CHAR_COUNT_Y * src_pages, 1):
        for i in range(0, CHAR_COUNT_X, 1):
            indent = 1 if WITH_INITIAL_INDENT else 0

            x1 = indent + i * (CHAR_WIDTH_PX + 1)
            y1 = indent + j * (CHAR_HEIGHT_PX + 1)
            x2 = x1 + CHAR_WIDTH_PX
            y2 = y1 + CHAR_HEIGHT_PX

            char_img = src_img.crop(
                (
                    x1,
                    y1,
                    x2,
                    y2,
                )
            )

            dst_img.paste(
                char_img,
                (
                    i * CHAR_WIDTH_PX,
                    j * CHAR_HEIGHT_PX,
                ),
            )

    dst_img = dst_img.resize(
        (
            dst_img.width * DST_SCALE_FACTOR,
            dst_img.height * DST_SCALE_FACTOR,
        ),
        Image.Resampling.NEAREST
    )

    dst_img.save(src_img_path.name + "_template.png")

if __name__ == "__main__":
    main()
