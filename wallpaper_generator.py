from PIL import Image, ImageDraw, ImageFont # ImageFont is needed for text
import ctypes
import os

class WallpaperGenerator:
    def __init__(self):
        user32 = ctypes.windll.user32
        self.screen_width = user32.GetSystemMetrics(0)
        self.screen_height = user32.GetSystemMetrics(1)
        print(f"wallpaperGenerator initialized. detected screen resolution: {self.screen_width}x{self.screen_height}")

        self.font_path = "Lexend-Regular.ttf"
        try:
            ImageFont.truetype(self.font_path, 1)
        except IOError:
            print(f"warning: font '{self.font_path}' not found")
            self.font_path = None

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

    def wrap_text(self, text, font, max_width):
        lines = []
        words = text.split(' ')
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.getlength(test_line) <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return lines

    def get_text_size_and_position(self, draw, text_lines, max_width, max_height, min_font_size=20, max_font_size=40):
        best_font_size = min_font_size
        best_lines = []
        final_font = None

        for font_size in range(min_font_size, max_font_size + 1):
            try:
                if self.font_path:
                    font = ImageFont.truetype(self.font_path, font_size)
                else:
                    font = ImageFont.load_default(font_size // 10)

                wrapped_lines = self.wrap_text("\n".join(text_lines), font, max_width)
                line_heights = [font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_lines]
                total_text_height = sum(line_heights)
                total_text_height += (len(wrapped_lines) - 1) * (font_size * 0.2)

                if total_text_height <= max_height:
                    best_font_size = font_size
                    best_lines = wrapped_lines
                    final_font = font
                else:
                    break
            except Exception as e:
                print(f"font loading/sizing error for size {font_size}: {e}")
                break

        if not final_font:
            if self.font_path:
                final_font = ImageFont.truetype(self.font_path, min_font_size)
            else:
                final_font = ImageFont.load_default(min_font_size // 10)
            
            best_lines = self.wrap_text("\n".join(text_lines), final_font, max_width)
            line_heights = [final_font.getbbox(line)[3] - final_font.getbbox(line)[1] for line in best_lines]
            total_text_height = sum(line_heights)
            total_text_height += (len(best_lines) - 1) * (min_font_size * 0.2)


        start_y = (self.screen_height - total_text_height) / 2
        return best_lines, final_font, start_y


    def generate_wallpaper_image(self, color1_hex, color2_hex, quote_text, output_path):
        img = Image.new('RGB', (self.screen_width, self.screen_height))
        draw = ImageDraw.Draw(img)

        start_rgb = self.hex_to_rgb(color1_hex)
        end_rgb = self.hex_to_rgb(color2_hex)

        for y in range(self.screen_height):
            factor = y / self.screen_height
            interpolated_rgb = self.interpolate_color(start_rgb, end_rgb, factor)
            draw.line([(0, y), (self.screen_width, y)], fill=interpolated_rgb)

        if quote_text:
            text_margin_x = int(self.screen_width * 0.05)
            text_margin_y = int(self.screen_height * 0.05)

            text_max_width = self.screen_width - (2 * text_margin_x)
            text_max_height = self.screen_height - (2 * text_margin_y)

            initial_lines_from_quote = quote_text.split('\n')
            wrapped_lines, font, start_y = self.get_text_size_and_position(
                draw, initial_lines_from_quote, text_max_width, text_max_height
            )

            start_y = text_margin_y

            current_y = start_y
            for line in wrapped_lines:
                text_bbox = draw.textbbox((0,0), line, font=font)
                text_width = text_bbox[2] - text_bbox[0]

                x = (self.screen_width - text_width) / 2
                draw.text((x, current_y), line, font=font, fill="white")
                
                line_height = text_bbox[3] - text_bbox[1]
                current_y += line_height + (font.size * 0.2)

        img.save(output_path, "PNG")
        print(f"generated wallpaper image saved to: {output_path}")
        return output_path