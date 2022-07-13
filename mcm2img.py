from pathlib import Path
from PIL import Image, ImageDraw
from sys import argv

resize_factor = 2

char_width = 12
char_height = 18
num_chars_max = 512
chars_per_page = 256

out = Image.new("RGBA", (char_width, char_height * num_chars_max), (0, 0, 0, 0))
draw = ImageDraw.Draw(out)
char = 0
x = 0
y = 0
skip = 0

if len(argv) > 6:
    font_r = int(argv[4])
    font_g = int(argv[5])
    font_b = int(argv[6])
else:
    font_r = int(255)
    font_g = int(255)
    font_b = int(255)

# This image format is really simple. It's binary-coded-ASCII (i.e., ASCII line `01100110` translates directly to a byte with these bit values). Each 2-bit nibble represents a pixel value.
# Instead of doing a lot of gymnastics to turn the ASCII to bytes and run through the bytes, it's easier to just read the ASCII pixel values directly and draw them into an image canvas.
# Each character is 12x18 characters, meaning 216 nibbles or 54 bytes (lines). But the MAX7456 memory is 64-byte aligned, so 10 bytes (lines) are wasted after each character.
# We do the same by just skipping 10 lines from the input between characters (again, we avoid having to do any parsing gymanstics this way).

with open(argv[1]) as f:
    for line in f:
        line = line.strip()
        if line == "MAX7456":
            continue
        if skip > 0:
            skip -= 1
            continue
        for pixel in (line[i:i+2] for i in range(0, len(line), 2)):
            if pixel == "00": # Black
                draw.point((x ,y + (char * char_height)), (0, 0, 0, 255))
            if pixel == "01": # Transparent
                draw.point((x ,y + (char * char_height)), (0, 0, 0, 0))
            if pixel == "10": # White
                draw.point((x, y + (char * char_height)), (font_r, font_g, font_b, 255))
            if pixel == "11": # Transparent + White
                draw.point((x, y + (char * char_height)), (font_r, font_g, font_b, 0))
            x += 1
            if x == char_width:
                y += 1
                x = 0
            if y == char_height:
                skip = 10
                char += 1
                y = 0

font1 = out.crop((0, 0, char_width, char_height * chars_per_page))
font2 = out.crop((0, char_height * chars_per_page, char_width, chars_per_page * 2 * char_height))

resize_factor = 2
out1_hd = font1.resize((char_width * resize_factor, char_height * chars_per_page * resize_factor), Image.NEAREST)
out2_hd = font2.resize((char_width * resize_factor, char_height * chars_per_page * resize_factor), Image.NEAREST)

resize_factor = 3
out1 = font1.resize((char_width * resize_factor, char_height * chars_per_page * resize_factor), Image.NEAREST)
out2 = font2.resize((char_width * resize_factor, char_height * chars_per_page * resize_factor), Image.NEAREST)

if len(argv) > 3:
    Path(argv[2] + "_hd.bin").write_bytes(out1_hd.tobytes('raw',argv[3]))
    Path(argv[2] + "_hd_2.bin").write_bytes(out2_hd.tobytes('raw',argv[3]))
    Path(argv[2] + ".bin").write_bytes(out1.tobytes('raw',argv[3]))
    Path(argv[2] + "_2.bin").write_bytes(out2.tobytes('raw',argv[3]))
else:
    out1.save(argv[2])
    out2.save("2_" + argv[2])
