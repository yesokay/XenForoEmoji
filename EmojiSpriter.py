#!/usr/bin/env python
import json
import time
import xml.etree.cElementTree as ET

'''
===
Create Emoji sprite sheets for XenForo based on the wonderful _emoji-data_ repo
https://github.com/iamcal/emoji-data
===
March 23, 2016
Andy Zhang
===

1. 'name' title cased becomes 'title'
2. 'image_url' is pre-set
3. 'w' and 'h' is pre-set
4. 'x' and 'y' are calculated from 'sheet_x' and 'sheet_y' values multiplied by emojis' pixel size * -1
5. 'smilie_text' comes from 'short_names[0]' surrounded by :

'''

## SET YOUR VARIABLES HERE

json_file = 'emoji.json'       # shouldn't need to be touched
img_file = '/styles/default/xenforo/emoji.png'      # relative path to your PNG file
pixels = 20                    # how wide/tall is each Emoji square
smilie_category_id = 1
sheet_title = 'Emoji Smilies'
new_filename = 'emojione/EmojiSmilies.xml'
style = 'emojione' # Available variants: apple, google, twitter, emojione

## THAT'S ALL. NO EDITS ARE NECESSARY BEYOND THIS LINE.
## If fact, don't edit anything below unless you know what you're doing.


# Initializations

start_at = time.time()
emojis = [] # In here goes the dictionaries for each emoji

# Parse the json
source = json.load(open(json_file), cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None)

if source != None:
    counter = 0

    for emoji in source:
        if emoji["has_img_"+style] is True:

            entry = {}
            entry["name"] = str(emoji["name"]).title()
            entry["x_val"] = emoji["sheet_x"] * pixels * -1
            entry["y_val"] = emoji["sheet_y"] * pixels * -1
            entry["short_name"] = ":" + emoji["short_names"][0] + ":"
            entry["side"] = str(pixels)

            emojis.append(entry)
            counter += 1
    print "%d emojis parsed." % counter


# Put all this in XML
root = ET.Element("smilies_export")

header = ET.SubElement(root, "smilie_categories")
ET.SubElement(header, "smilie_category", id = str(smilie_category_id), title = sheet_title, display_order = "10")

body = ET.SubElement(root, "smilies")


# For each smilie
i = 0
item = emojis
# Add an entry
for entry in emojis:
    item[i] = ET.SubElement(body, "smilie", smilie_category_id = str(smilie_category_id), title = entry["name"], display_order = "10", display_in_editor = "1")
    ET.SubElement(item[i], "image_url").text = img_file
    ET.SubElement(item[i], "sprite_params", w = entry["side"], h = entry["side"], x = str(entry["x_val"]), y = str(entry["y_val"]))
    ET.SubElement(item[i], "smilie_text").text = entry["short_name"]
    i += 1


# Boom
tree = ET.ElementTree(root)
tree.write(new_filename, encoding="utf-8", xml_declaration=True)

print "Done in %s seconds. Please see %s." % (round(time.time() - start_at, 3), new_filename)

