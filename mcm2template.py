from pathlib import Path
from PIL import Image, ImageDraw
from sys import argv


CHAR_WIDTH = 12
CHAR_HEIGHT = 18

CHAR_COUNT_X = 16
CHAR_COUNT_Y = 16

SRC_SCALE_FACTOR = 3

DST_PAGES = 2
DST_SCALE_FACTOR = 3
DST_CHAR_COUNT = CHAR_COUNT_X * CHAR_COUNT_Y * DST_PAGES


def main():
    mcm_path = Path(argv[1])
    mcm_img = Image.new(
        "RGBA",
        (CHAR_COUNT_X * CHAR_WIDTH, CHAR_HEIGHT * CHAR_COUNT_Y * DST_PAGES),
        (0, 0, 0, 0),
    )
    mcm_img_draw = ImageDraw.Draw(mcm_img)

    with open(mcm_path) as f:
        template_x = 0
        template_y = 0
        char_x = 0
        char_y = 0
        skip_align = 0

        for line in f:
            line = line.strip()
            if line == "MAX7456":
                continue

            if skip_align > 0:
                skip_align -= 1
                continue

            for pixel in (line[i : i + 2] for i in range(0, len(line), 2)):
                mcm_img_draw.point(
                    (
                        (template_x * CHAR_WIDTH) + char_x,
                        (template_y * CHAR_HEIGHT) + char_y,
                    ),
                    {
                        "00": (0, 0, 0, 255),
                        "01": (0, 0, 0, 0),
                        "10": (255, 255, 255, 255),
                        "11": (255, 255, 255, 0),
                    }[pixel],
                )

                char_x += 1
                if char_x == CHAR_WIDTH:
                    char_y += 1
                    char_x = 0
                if char_y == CHAR_HEIGHT:
                    skip_align = 10
                    char_y = 0

                    template_x += 1
                    if template_x == CHAR_COUNT_X:
                        template_x = 0
                        template_y += 1

    mcm_img = mcm_img.resize(
        (mcm_img.width * DST_SCALE_FACTOR, mcm_img.height * DST_SCALE_FACTOR),
        Image.Resampling.NEAREST,
    )

    mcm_img.save(mcm_path.stem + "_template.png")


if __name__ == "__main__":
    main()
