from PIL import Image, ImageDraw
import ctypes
import os

class WallpaperGenerator:
    def __init__(self):
        user32 = ctypes.windll.user32
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)
        print(f"wallpaperGenerator initialized. detected screen resolution: {self.screen_width}x{self.screen_height}")


    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def interpolate_color(self, color1, color2, factor):
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        r = int(r1 + factor * (r2 - r1))
        g = int(g1 + factor * (g2 - g1))
        b = int(b1 + factor * (b2 - b1))
        return (r, g, b)

    def generate_wallpaper_image(self, color1_hex, color2_hex, quote_text, output_path):
        img = Image.new('RGB', (self.screen_width, self.screen_height))
        draw = ImageDraw.Draw(img)

        start_rgb = self.hex_to_rgb(color1_hex)
        end_rgb = self.hex_to_rgb(color2_hex)

        for y in range(self.screen_height):
            factor = y / self.screen_height
            interpolated_rgb = self.interpolate_color(start_rgb, end_rgb, factor)
            draw.line([(0, y), (self.screen_width, y)], fill=interpolated_rgb)

        img.save(output_path, "PNG")
        print(f"Generated wallpaper image saved to: {output_path}")
        return output_path

if __name__ == "__main__":
    print("running wallpaper_generator.py in test mode (no quotes).")
    generator = WallpaperGenerator()

    current_script_dir = os.path.dirname(__file__)
    test_output_path = os.path.join(current_script_dir, "test_gradient_wallpaper_no_quote.png")

    color_start = "#FF5733"
    color_end = "#337DFF"
    
    print(f"generating test image with colors {color_start} to {color_end} (no quote)")
    generated_path = generator.generate_wallpaper_image(color_start, color_end, "", test_output_path)
    print(f"test image generated at: {generated_path}")

    print("test finished for wallpaper_generator.py.")