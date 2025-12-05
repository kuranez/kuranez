import random
import os
import glob

# Define the absolute path to the project directory
project_dir = os.path.dirname(os.path.abspath(__file__))

# Configuration: Select franchises
# OPTIONS = ["all", ["south_park"], ["spongebob"], ["mass_effect"]]
# Set to "all" to use all franchises, or list specific ones: ["south_park", "spongebob"]
# Single franchise: ["mass_effect"]
SELECTED_FRANCHISES = ["all"]

# Construct paths
collection_dir = os.path.join(project_dir, "collection")
readme_file = os.path.join(project_dir, "README.md")

# Find character directories based on selection
if SELECTED_FRANCHISES == "all":
    # Find all franchise directories
    franchise_dirs = [d for d in glob.glob(os.path.join(collection_dir, "*")) if os.path.isdir(d)]
    # Find all character directories across all franchises
    character_dirs = []
    for franchise_dir in franchise_dirs:
        character_dirs.extend([d for d in glob.glob(os.path.join(franchise_dir, "*")) if os.path.isdir(d)])
else:
    # Use only selected franchises
    character_dirs = []
    for franchise_name in SELECTED_FRANCHISES:
        franchise_dir = os.path.join(collection_dir, franchise_name)
        if os.path.isdir(franchise_dir):
            character_dirs.extend([d for d in glob.glob(os.path.join(franchise_dir, "*")) if os.path.isdir(d)])

if not character_dirs:
    if SELECTED_FRANCHISES == "all":
        print("No character directories found in any franchise")
    else:
        print(f"No character directories found in {', '.join(SELECTED_FRANCHISES)}")
    exit(1)

# Choose a random character
selected_character_dir = random.choice(character_dirs)
# Extract franchise name from path for display and icon path
franchise_name = os.path.basename(os.path.dirname(selected_character_dir))
quotes_file = os.path.join(selected_character_dir, "quotes.txt")
icon_file = os.path.join(selected_character_dir, "icon.png")

# Load quotes with UTF-8 encoding
with open(quotes_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# First line is the author (format: "- Author Name")
author = lines[0].strip().replace("- ", "")

# Rest are quotes (skip empty lines)
# Remove all types of quotation marks: „ " " ' '
quotes = []
for line in lines[1:]:
    line = line.strip()
    if line and not line.startswith("-"):
        # Remove all quotation mark types
        cleaned = line.strip('„"""“\'\'')
        quotes.append(cleaned)

if not quotes:
    print(f"No quotes found for {author}")
    exit(1)

# Choose a random quote
quote = random.choice(quotes)

# Check if icon exists
icon_path_relative = f"collection/{franchise_name}/{os.path.basename(selected_character_dir)}/icon.png"
if not os.path.exists(icon_file):
    icon_path_relative = ""  # No icon available

# Generate HTML banner
html_banner = f'''<div align="center">
  <table>
    <tr>
      <td>'''

if icon_path_relative:
    html_banner += f'''
        <img src="{icon_path_relative}" alt="{author}" width="100" height="100">'''

html_banner += f'''
      </td>
      <td>
        <p style="font-size: 18px; color: #58A6FF; margin: 0;">{quote}</p>
        <p style="font-size: 14px; color: #8B949E; margin: 5px 0 0 0;">— {author}</p>
      </td>
    </tr>
  </table>
</div>'''

# Read the README
with open(readme_file, "r", encoding="utf-8") as readme:
    content = readme.read()

# Find the start and end of the quote section
start_marker = "<!--QUOTE_START-->"
end_marker = "<!--QUOTE_END-->"
start_index = content.find(start_marker)
end_index = content.find(end_marker)

# Build the new content
if start_index != -1 and end_index != -1:
    before_quote = content[:start_index + len(start_marker)]
    after_quote = content[end_index:]
    new_content = f"{before_quote}\n{html_banner}\n{after_quote}"
else:
    # If markers are not found, append the quote at the end
    new_content = content + f"\n{start_marker}\n{html_banner}\n{end_marker}\n"

# Write the new quote section
with open(readme_file, "w", encoding="utf-8") as readme:
    readme.write(new_content)

print(f"Successfully updated README.md with quote from {author} ({franchise_name})")
print(f"Quote: \"{quote}\"")
