import pyautogui as pag
import time
import os
import tkinter
import move
import loadsettings
import Quartz.CoreGraphics as CG
import struct
from logpy import log
ms = pag.size()
mw = ms[0]
mh = ms[1]
#0% 7697781
#31% 8381831
#52% 8502900
#84% 11231045
#100% 14889259
class ScreenPixel(object):
    """Captures the screen using CoreGraphics, and provides access to
    the pixel values.
    """

    def capture(self, region = None):
        """region should be a CGRect, something like:

        >>> import Quartz.CoreGraphics as CG
        >>> region = CG.CGRectMake(0, 0, 100, 100)
        >>> sp = ScreenPixel()
        >>> sp.capture(region=region)

        The default region is CG.CGRectInfinite (captures the full screen)
        """

        if region is None:
            region = CG.CGRectInfinite
        else:
            # TODO: Odd widths cause the image to warp. This is likely
            # caused by offset calculation in ScreenPixel.pixel, and
            # could could modified to allow odd-widths
            if region.size.width % 2 > 0:
                emsg = "Capture region width should be even (was %s)" % (
                    region.size.width)
                raise ValueError(emsg)

        # Create screenshot as CGImage
        image = CG.CGWindowListCreateImage(
            region,
            CG.kCGWindowListOptionOnScreenOnly,
            CG.kCGNullWindowID,
            CG.kCGWindowImageDefault)

        # Intermediate step, get pixel data as CGDataProvider
        prov = CG.CGImageGetDataProvider(image)

        # Copy data out of CGDataProvider, becomes string of bytes
        self._data = CG.CGDataProviderCopyData(prov)

        # Get width/height of image
        self.width = CG.CGImageGetWidth(image)
        self.height = CG.CGImageGetHeight(image)

    def pixel(self, x, y):
        """Get pixel value at given (x,y) screen coordinates

        Must call capture first.
        """

        # Pixel data is unsigned char (8bit unsigned integer),
        # and there are for (blue,green,red,alpha)
        data_format = "BBBB"

        # Calculate offset, based on
        # http://www.markj.net/iphone-uiimage-pixel-color/
        offset = 4 * ((self.width*int(round(y))) + int(round(x)))

        # Unpack data from string into Python'y integers
        b, g, r, a = struct.unpack_from(data_format, self._data, offset=offset)

        # Return BGRA as RGBA
        return (r, g, b, a)


def rgb_to_hex(r, g, b):
      return ('0x{:X}{:X}{:X}').format(r, g, b)
def bpc():
    dt = loadsettings.load()['display_type']
    X1=mw//2+63
    Y1=8
    if dt == "built-in retina display":
        X1= (mw//2+63)*2 #(round((mw/2+60), 0))*2
        Y1= 8*2 #14*2
    sp = ScreenPixel()
    sp.capture()
    col = sp.pixel(X1, Y1)
    backpackColor = int(rgb_to_hex(col[0],col[1],col[2]),16)
    #gm = 0.00001284664 #100/(14889259-7105124)
    #gc = -91.276 #100- gm*14889259
    #perc = int(gm*backpackColor+gc)

    if backpackColor >= 14889259: #13775147
        perc = 100
    elif backpackColor >= 11231045:
        perc = 85
    elif backpackColor >= 8502900:
        perc = 50
    elif backpackColor >= 8381831:
        perc = 30
    else:
        perc = 0
    #print("Pixel Colour: {}, Backpack Percentage: {}.".format(backpackColor, perc))
    log("Pixel Colour: {}, Backpack Percentage: {}.".format(backpackColor, perc))
    return perc


