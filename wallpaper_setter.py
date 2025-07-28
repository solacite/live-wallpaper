import ctypes
import os
import time

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

def set_wallpaper(image):
    if not os.path.exists(image):
        print(f"error: image file not found at {image}")
        return False
    
    abs_image = os.path.abspath(image).encode('utf-8')

    result = ctypes.windll.user32.SystemParametersInfoA(
            SPI_SETDESKWALLPAPER,
            0,
            abs_image,
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    )

    if result:
        print(f"wallpaper set to: {image}")
        return True
    else:
        print(f"failed to set wallpaper. Error code: {ctypes.GetLastError()}")
        return False
    