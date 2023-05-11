from PIL import Image, ImageDraw

char_width = 12
char_height = 18

chars_x = 16
chars_y = 16


def gen(pages):
    img = Image.new(
        "RGBA", (char_width * chars_x, char_height * chars_y * pages), (0, 0, 0, 0)
    )
    draw = ImageDraw.Draw(img)

    for i in range(0, chars_x, 1):
        for j in range(0, chars_y * pages, 1):
            if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                x1 = i * char_width
                y1 = j * char_height
                x2 = x1 + char_width - 1
                y2 = y1 + char_height - 1
                rect = (x1, y1, x2, y2)

                draw.rectangle(
                    rect,
                    (255, 255, 255, 255),
                )

    return img


double_page_img = gen(2)
double_page_img = double_page_img.resize(
    (double_page_img.width * 3, double_page_img.height * 3), Image.Resampling.NEAREST
)
double_page_img.save("template_overlay.png")
