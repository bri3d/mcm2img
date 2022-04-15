# MCM2IMG

Converts Maxim analog video overlay (for example, Betaflight and iNAV OSD) fonts to desired image format.

The Maxim format is documented here: https://www.maximintegrated.com/en/design/technical-documents/app-notes/4/4117.html

Useful for: previewing fonts, converting fonts for use in other applications, etc.

# Use

python3 mcm2img.py mcmfile.mcm imagefile.fmt [rawfmt] [R] [G] [B]
eg : python3 mcm2img.py mcmfile.mcm imagefile.fmt [rawfmt] 0 255 0 for green font colour


if rawfmt is specified, it's one of the (many) raw bitmap formats supported by Pillow: https://github.com/python-pillow/Pillow/blob/main/src/libImaging/Unpack.c#L1483 . RGBA is probably the most common thing you will want here.
