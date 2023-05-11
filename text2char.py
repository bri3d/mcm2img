from PIL import Image, ImageDraw, ImageFont
import colorsys


CHARS = [chr(x) for x in range(ord(" "), ord("_") + 1)]

CHAR_WIDTH = 12 * 3
CHAR_HEIGHT = 18 * 3

CHAR_COUNT_X = 16
CHAR_COUNT_Y = len(CHARS) // CHAR_COUNT_X

SRC_SCALE_FACTOR = 3


def hsv_to_rgb(h, s, v):
    return tuple(int(c * 255) for c in colorsys.hsv_to_rgb(h, s, v))


def main():
    img = Image.new(
        "RGBA", (CHAR_WIDTH * CHAR_COUNT_X, CHAR_HEIGHT * CHAR_COUNT_Y), (0, 0, 0, 0)
    )

    img_draw = ImageDraw.Draw(img)

    for i, char in enumerate(CHARS):
        x = i % CHAR_COUNT_X * CHAR_WIDTH
        y = i // CHAR_COUNT_X * CHAR_HEIGHT

        img_draw.text(
            (x + CHAR_WIDTH // 2, y + CHAR_HEIGHT // 2),
            char,
            fill=hsv_to_rgb(i / len(CHARS), 0.5, 1),
            font=ImageFont.truetype("NotoMono-Regular.ttf", CHAR_WIDTH),
            anchor="mm",
            stroke_width=2,
            stroke_fill=(0, 0, 0, 255),
        )

    img.save("text.png")


if __name__ == "__main__":
    main()
