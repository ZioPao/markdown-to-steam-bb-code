import re

def markdown_to_bbcode(markdown_text):
    # Regular expressions to match Markdown elements
    bold_regex = r'\*\*(.*?)\*\*'
    italic_regex = r'\*(.*?)\*'
    code_regex = r'`([^`]+)`'
    header_regex = r'^(#+)\s*(.*?)$'
    link_regex = r'\[([^\]]+)\]\(([^\)]+)\)'

    # Dictionary to hold the translations of Markdown to BBCODE elements
    markdown_to_bbcode = {
        bold_regex: r'[b]\1[/b]',
        italic_regex: r'[i]\1[/i]',
        code_regex: r'[code]\1[/code]',
        header_regex: lambda match: f"[h1]{match.group(2)}[/h1]",
        link_regex: r'[url=\2]\1[/url]',
    }
    # [url=https://ko-fi.com/M4M7IERNW][img]https://storage.ko-fi.com/cdn/kofi3.png[/img][/url]

    # Applying the regular expressions for translation
    bbcode_text = markdown_text
    for markdown_regex, bbcode_replacement in markdown_to_bbcode.items():
        if callable(bbcode_replacement):
            bbcode_text = re.sub(markdown_regex, bbcode_replacement, bbcode_text, flags=re.MULTILINE)
            #print(bbcode_replacement)
            #print(bbcode_text)
        else:
            bbcode_text = re.sub(markdown_regex, bbcode_replacement, bbcode_text)

    return bbcode_text

import os
import sys
if __name__ == "__main__":

    try:
        user = sys.argv[1]
        workspace = sys.argv[2]      # ${workspaceFolderBasename}
    except IndexError:
        print("You didn't pass the correct parameter.")
        exit()

    zomboid_folder = "C:\\Users\\" + user + "\\Zomboid"

    mod_folder = os.path.join(zomboid_folder, "mods", workspace)
    input = os.path.join(mod_folder, "README.md")

    # get main readme.MD
    with open(input, "r") as f:
        markdown_text = f.read()
        bbcode_text = markdown_to_bbcode(markdown_text)
        bbcode_lines = bbcode_text.split("\n")
        
        is_list = False
        for i in range(len(bbcode_lines)):
            # match line with images
            # [url=https://ko-fi.com/M4M7IERNW][img]https://storage.ko-fi.com/cdn/kofi3.png[/img][/url]
            img_pattern = r'\[url=([^\]]+\.(?:gif|png|jpg|svg))\]([^/]+)\[/url\]'
            if re.match(img_pattern, bbcode_lines[i]):
                image_url = re.search(img_pattern, bbcode_lines[i]).group(1)
                #print(image_url)

                url_pattern = r'\[url=.*?\]\(([^)]+)\)'
                if re.match(url_pattern, bbcode_lines[i]):
                    actual_url = re.search(url_pattern, bbcode_lines[i]).group(1)
                    #print(actual_url)
                    modified_img_string = f"[url={actual_url}][img]{image_url}[/img][/url]"
                    bbcode_lines[i] = modified_img_string

            # check lists
            if is_list:
                print("is_list")
                if bbcode_lines[i].startswith("- "):
                    print(bbcode_lines[i])
                    bbcode_lines[i]  = f"[*]{bbcode_lines[i][1:]}"
                else:
                    bbcode_lines[i]  = "[/list]\n"
                    is_list  = False

            if bbcode_lines[i].startswith("- ") and is_list == False:
                is_list = True
                bbcode_lines[i] = f"[list]\n[*]{bbcode_lines[i][1:]}"




        # write to .bb file in the out directory
        bbcode_text = "\n".join(bbcode_lines)

        output_path = os.path.join(mod_folder, "workshop_files", "workshop_desc.bb")
        with open(output_path, "w") as out_file:
            out_file.write(bbcode_text)
