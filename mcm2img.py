from pathlib import Path
from PIL import Image, ImageDraw
from sys import argv

out = Image.new("RGBA", (3072, 18), (0, 0, 0, 0))
draw = ImageDraw.Draw(out)
char = 0
x = 0
y = 0
skip = 0

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
                draw.point((x + (char * 12), y), (0, 0, 0, 255))
            if pixel == "01": # Transparent
                draw.point((x + (char * 12), y), (0, 0, 0, 0))
            if pixel == "10": # White
                draw.point((x + (char * 12), y), (255, 255, 255, 255))
            if pixel == "11": # Transparent + White
                draw.point((x + (char * 12), y), (255, 255, 255, 0))
            x += 1
            if x == 12:
                y += 1
                x = 0
            if y == 18:
                skip = 10
                char += 1
                y = 0
          
if len(argv) > 3:
    Path(argv[2]).write_bytes(out.tobytes('raw',argv[3]))
else:
    out.save(argv[2])