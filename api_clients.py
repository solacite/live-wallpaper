import requests
import json
import random

class ColorApiClient:
    def __init__(self):
        self.api_url = "https://www.thecolorapi.com/scheme"

    def get_gradient_colors(self):
        print("fetching colors from TheColorAPI...")
        try:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)

            seed_hex_color = f"{r:02x}{g:02x}{b:02x}".upper()
            print(f"using random seed color: #{seed_hex_color}")

            params = {
                'hex': seed_hex_color,
                'mode': 'analogic',
                'count': 2
            }
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()

            data = response.json()
            colors_data = data.get('colors')

            if colors_data and len(colors_data) >= 2:
                color1_hex = colors_data[0]['hex']['value']
                color2_hex = colors_data[1]['hex']['value']

                print(f"successfully fetched colors: {color1_hex}, {color2_hex}")
                return color1_hex, color2_hex
            else:
                print("API response did not contain enough valid colors")
                raise ValueError("insufficient colors from API")

        except (requests.exceptions.RequestException, ValueError, KeyError, json.JSONDecodeError) as e:
            print(f"error fetching colors from API: {e}.")
            return "#3498db", "#8e44ad"

class QuoteApiClient:
    def __init__(self):
        self.api_url = 'https://zenquotes.io/api/random'

    def get_random_quote(self):
        print("fetching a random quote from zen API...")
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()

            data = response.json()
            
            if data and isinstance(data, list) and len(data) > 0:
                quote_obj = data[0]
                quote_content = quote_obj.get('q', '')
                quote_author = quote_obj.get('a', 'Unknown')

                if quote_content:
                    formatted_quote = f"“{quote_content}”\n– {quote_author}"
                    print(f"QuoteApiClient: Successfully fetched quote: '{quote_content[:50]}...'")
                    return formatted_quote
                else:
                    print("QuoteApiClient: API returned empty content. Falling back to default quote.")
                    raise ValueError("Empty quote content from API")
            else:
                print("QuoteApiClient: API returned no quotes. Falling back to default quote.")
                raise ValueError("No quotes returned from API")
        except (requests.exceptions.RequestException, ValueError, KeyError, json.JSONDecodeError) as e:
                print(f"error fetching quote from API: {e}")
                return "womp womp"

