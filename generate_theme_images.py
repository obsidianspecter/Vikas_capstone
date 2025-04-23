from PIL import Image, ImageDraw, ImageFont
import os

# Create directory for images if it doesn't exist
os.makedirs('static/images', exist_ok=True)

# Theme data with names and colors
themes = [
    # Original themes
    {'name': 'dark-theme', 'bg_color': '#1a1a1a', 'accent_color': '#0080ff'},
    {'name': 'light-theme', 'bg_color': '#f8f8f8', 'accent_color': '#0080ff'},
    {'name': 'orange-theme', 'bg_color': '#331100', 'accent_color': '#ff7700'},
    {'name': 'blue-theme', 'bg_color': '#003366', 'accent_color': '#0066cc'},
    {'name': 'green-theme', 'bg_color': '#003300', 'accent_color': '#006633'},
    
    # New color themes
    {'name': 'purple-theme', 'bg_color': '#240046', 'accent_color': '#5a189a'},
    {'name': 'red-theme', 'bg_color': '#370617', 'accent_color': '#d00000'},
    {'name': 'teal-theme', 'bg_color': '#023e8a', 'accent_color': '#0096c7'},
    {'name': 'amber-theme', 'bg_color': '#7f4f24', 'accent_color': '#ca6702'},
    {'name': 'pink-theme', 'bg_color': '#590d22', 'accent_color': '#ff758f'},
    
    # Dark variations
    {'name': 'midnight-theme', 'bg_color': '#121212', 'accent_color': '#1a237e'},
    {'name': 'dark-forest-theme', 'bg_color': '#1c1c1c', 'accent_color': '#2d3b2d'},
    {'name': 'dark-chocolate-theme', 'bg_color': '#1c1c1c', 'accent_color': '#3e2723'},
    {'name': 'amoled-theme', 'bg_color': '#000000', 'accent_color': '#2196f3'},
    
    # Light variations
    {'name': 'cream-theme', 'bg_color': '#f9f5f0', 'accent_color': '#e6ccb2'},
    {'name': 'mint-theme', 'bg_color': '#effffd', 'accent_color': '#9be3de'},
    {'name': 'lavender-theme', 'bg_color': '#f5f0ff', 'accent_color': '#b8a9c9'},
    
    # Special themes
    {'name': 'high-contrast-theme', 'bg_color': '#000000', 'accent_color': '#ffff00'},
    {'name': 'retro-theme', 'bg_color': '#000000', 'accent_color': '#00ff00'},
    {'name': 'cyberpunk-theme', 'bg_color': '#000033', 'accent_color': '#ff00ff'},
    {'name': 'monochrome-theme', 'bg_color': '#000000', 'accent_color': '#333333'},
    {'name': 'pastel-theme', 'bg_color': '#feeafa', 'accent_color': '#ffafcc'},
    
    # Seasonal themes
    {'name': 'winter-theme', 'bg_color': '#caf0f8', 'accent_color': '#48cae4'},
    {'name': 'autumn-theme', 'bg_color': '#fefae0', 'accent_color': '#bc6c25'},
    {'name': 'spring-theme', 'bg_color': '#f8edeb', 'accent_color': '#ff8fab'},
    {'name': 'summer-theme', 'bg_color': '#fdffb6', 'accent_color': '#ff9e00'},
]

# Generate images for each theme
for theme in themes:
    # Create a new image with the theme's background color
    img = Image.new('RGB', (400, 200), theme['bg_color'])
    draw = ImageDraw.Draw(img)
    
    # Draw a rectangle with the accent color
    draw.rectangle([(50, 50), (350, 150)], fill=theme['accent_color'])
    
    # Try to add text (requires font)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
        draw.text((200, 100), theme['name'], fill='white', font=font, anchor="mm")
    except:
        # If font not available, just draw without text
        pass
    
    # Save the image
    img.save(f"static/images/{theme['name']}.png")
    print(f"Generated {theme['name']}.png")

print("All theme images generated successfully!")