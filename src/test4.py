from modules import bitmap_matcher
from PIL import Image

countBitmaps = []
bearMorphs = []
hasteBitmap = Image.new('RGBA', (10, 1), '#f0f0f0ff')
melodyBitmap = Image.new('RGBA', (3, 2), '#2b2b2bff')
countBitmaps.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAAQAAAALCAAAAAB9zHN3AAAAAnRSTlMAAHaTzTgAAABCSURBVHgBATcAyP8BAPMAAADzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPMAAADzAAAA8wAAAPMAAAAB8wAAAAIAAAAAtc8GqohTl5oAAAAASUVORK5CYII=")) #2
countBitmaps.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAAQAAAAKCAAAAAC2kKDSAAAAAnRSTlMAAHaTzTgAAAA9SURBVHgBATIAzf8BAPMAAAAAAAAAAAAAAAAAAAAAAAAAAADzAAAAAAAAAAAAAAAAAAAAAPMAAAABAPMAAFILA8/B68+8AAAAAElFTkSuQmCC"))
countBitmaps.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAAQAAAAGCAAAAADBUmCpAAAAAnRSTlMAAHaTzTgAAAApSURBVHgBAR4A4f8AAAAA8wAAAAAAAAAA8wAAAPMAAALzAAAAAfMAAABBtgTDARckPAAAAABJRU5ErkJggg=="))
countBitmaps.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAAQAAAALCAAAAAB9zHN3AAAAAnRSTlMAAHaTzTgAAABCSURBVHgBATcAyP8B8wAAAAIAAAAAAPMAAAACAAAAAAHzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHzAAAAgmID1KbRt+YAAAAASUVORK5CYII="))
countBitmaps.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAAQAAAAJCAAAAAAwBNJ8AAAAAnRSTlMAAHaTzTgAAAA4SURBVHgBAS0A0v8AAAAA8wAAAPMAAADzAAACAAAAAAEA8wAAAPPzAAAA8wAAAAAA8wAAAQAA8wC5oAiQ09KYngAAAABJRU5ErkJggg=="))
countBitmaps.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAAQAAAAMCAAAAABgyUPPAAAAAnRSTlMAAHaTzTgAAABHSURBVHgBATwAw/8B8wAAAAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA8wIAAAAAAgAAAABDdgHu70cIeQAAAABJRU5ErkJggg=="))
countBitmaps.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAAQAAAAKCAAAAAC2kKDSAAAAAnRSTlMAAHaTzTgAAAA9SURBVHgBATIAzf8BAADzAAAA8wAAAgAAAAABAPMAAAEAAPMAAADzAAAAAAAAAADzAAAAAADzAAABAADzALv5B59oKTe0AAAAAElFTkSuQmCC"))
countBitmaps.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAAQAAAAKCAAAAAC2kKDSAAAAAnRSTlMAAHaTzTgAAAA9SURBVHgBATIAzf8BAADzAAAA8wAAAPMAAAAAAPMAAAEAAPMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA87TcBbXcfy3eAAAAAElFTkSuQmCC"))
countBitmaps.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAAgAAAAKCAAAAACsrEBcAAAAAnRSTlMAAHaTzTgAAAArSURBVHgBY2Rg+MzAwMALxCAaQoDBZyYYmwlMYmXAAFApWPVnBkYIi5cBAJNvCLCTFAy9AAAAAElFTkSuQmCC")) #0

bearMorphs.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAAwAAAABBAMAAAAYxVIKAAAAD1BMVEUwLi1STEihfVWzpZbQvKTt7OCuAAAAEklEQVR4AQEHAPj/ACJDEAE0IgLvAM1oKEJeAAAAAElFTkSuQmCC"))
bearMorphs.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAA4AAAABBAMAAAAcMII3AAAAFVBMVEUwLi1TTD9lbHNmbXN5enW5oXHQuYJDhTsuAAAAE0lEQVR4AQEIAPf/ACNGUQAVZDIFbwFmjB55HwAAAABJRU5ErkJggg=="))
bearMorphs.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAABAAAAABBAMAAAAlVzNsAAAAGFBMVEUwLi1VU1G9u7m/vLXAvbbPzcXg3dfq6OXkYMPeAAAAFElEQVR4AQEJAPb/AENWchABJ2U0CO4B3TmcTKkAAAAASUVORK5CYII="))
bearMorphs.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAA4AAAABBAMAAAAcMII3AAAAElBMVEUwLi1JSUqOlZy0vMbY2dnc3NtuftTJAAAAE0lEQVR4AQEIAPf/AFVDIQASNFUFhQFVdZ1AegAAAABJRU5ErkJggg=="))
bearMorphs.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAAA4AAAABBAMAAAAcMII3AAAAFVBMVEUwLi1TTD+zjUy0jky8l1W5oXHevny+g95vAAAAE0lEQVR4AQEIAPf/ACNGUQAVZDIFbwFmjB55HwAAAABJRU5ErkJggg=="))
bearMorphs.append(bitmap_matcher.create_bitmap_from_base64("iVBORw0KGgoAAAANSUhEUgAAABAAAAABBAMAAAAlVzNsAAAAJFBMVEVBNRlDNxtTRid8b0avoG69r22+sG7Qw4PRw4Te0Jbk153m2Z5VNHxxAAAAFElEQVR4AQEJAPb/AFVouTECSnZVDPsCv+2QpmwAAAAASUVORK5CYII="))

hastePlus = Image.new('RGBA', (20, 1), '#eddb4cff')

screen = Image.open("screenshot.png").convert('RGBA')

x = 0
hasteX = False
#locate haste. It shares the same color as melody
for _ in range(3):
    res = bitmap_matcher.find_bitmap_cython(screen, hasteBitmap, x=x, variance=0)
    if not res:
        break
    x = res[0]
    #can't find melody, so its haste
    if not bitmap_matcher.find_bitmap_cython(screen, melodyBitmap, x=x+2, w=16, variance=2):
        hasteX = res[0]
        break
    #melody, skip this buff
    x+= 40

print(hasteX)
#haste found, get count
if hasteX:
    for i, img in enumerate(countBitmaps):
        res = bitmap_matcher.find_bitmap_cython(screen, img, x=hasteX, w=38, variance=0)
        if res:
            haste = i+2
            break
    else:
        haste = 1

for img in bearMorphs:
    if bitmap_matcher.find_bitmap_cython(screen, img, variance=30):
        print("hey")
        break

if bitmap_matcher.find_bitmap_cython(screen, hastePlus, variance=20 if False else 2):
    print("lol")