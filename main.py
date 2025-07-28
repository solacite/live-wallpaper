import os
import time
import threading

from wallpaper_setter import set_wallpaper
from api_clients import ColorApiClient, QuoteApiClient
from wallpaper_generator import WallpaperGenerator

TEMP_WALLPAPER_DIR = os.path.join(os.path.expanduser("~"), "Documents", "LiveWallpaperApp")
TEMP_WALLPAPER_PATH = os.path.join(TEMP_WALLPAPER_DIR, "current_wallpaper.png")

os.makedirs(TEMP_WALLPAPER_DIR, exist_ok=True)
print(f"temporary wallpaper will be saved to: {TEMP_WALLPAPER_PATH}")

UPDATE_INTERVAL_SECONDS = 30 * 60

color_client = ColorApiClient()
quote_client = QuoteApiClient()
wallpaper_generator = WallpaperGenerator()

def update_wallpaper():
    print(f"\n--- Initiating wallpaper update at {time.ctime()} ---")
    try:
        color1, color2 = color_client.get_gradient_colors()

        quote_text = quote_client.get_random_quote()

        print("Generating new wallpaper image...")
        generated_image_path = wallpaper_generator.generate_wallpaper_image(
            color1, color2, quote_text, TEMP_WALLPAPER_PATH
        )
        print(f"generated image path: {generated_image_path}")

        set_wallpaper(generated_image_path)

    except Exception as e:
        print(f"an error occurred during wallpaper update: {e}")
        import traceback
        traceback.print_exc()

def schedule_wallpaper_update():

    update_wallpaper()

    timer = threading.Timer(UPDATE_INTERVAL_SECONDS, schedule_wallpaper_update)
    timer.daemon = True
    timer.start()
    print(f"next wallpaper update scheduled in {UPDATE_INTERVAL_SECONDS / 60} minutes.")

if __name__ == "__main__":
    print("live wallpaper app starting...")
    print(f"wallpaper will update automatically every {UPDATE_INTERVAL_SECONDS / 60} minutes.")
    print("to stop the app, close this terminal window or press Ctrl+C.")

    schedule_wallpaper_update()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nlive wallpaper app stopped by user (Ctrl+C).")
    except Exception as e:
        print(f"an unexpected error occurred in the main loop: {e}")