import os
import re
from pathlib import Path
from xml.etree import ElementTree as ET

# Keywords to remove from filenames
REMOVE_PATTERNS = [
    r'\b(xvid|bluray|blu-ray|720p|1080p|2160p|hdr|webrip|dvdrip|hdtv|brrip|web-dl|hevc|h\.264|x264|x265)\b',
    r'\.mkv$|\.mp4$|\.avi$|\.mov$',  # remove extensions
    r'\W+',  # clean up extra symbols/spaces
]

def clean_filename(filename: str) -> str:
    name = filename.lower()
    for pattern in REMOVE_PATTERNS:
        name = re.sub(pattern, ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name.title()

def update_nfo_title(nfo_path: Path, new_title: str):
    try:
        tree = ET.parse(nfo_path)
        root = tree.getroot()

        title_elem = root.find('title')
        if title_elem is not None:
            old_title = title_elem.text
            title_elem.text = new_title
            print(f"Updated: '{old_title}' -> '{new_title}'")
        else:
            title_elem = ET.SubElement(root, 'title')
            title_elem.text = new_title
            print(f"Added title: '{new_title}'")

        tree.write(nfo_path, encoding='utf-8', xml_declaration=True)
    except ET.ParseError as e:
        print(f"XML Parse Error in {nfo_path}: {e}")

def process_directory(directory: str):
    for dirpath, _, filenames in os.walk(directory):
        video_files = [f for f in filenames if f.lower().endswith(('.mkv', '.mp4', '.avi', '.mov'))]

        for video in video_files:
            video_path = Path(dirpath) / video
            base_name = video_path.stem
            cleaned_title = clean_filename(video)

            nfo_path = video_path.with_suffix('.nfo')
            if nfo_path.exists():
                update_nfo_title(nfo_path, cleaned_title)
            else:
                print(f"Missing NFO for: {video}")

if __name__ == "__main__":
    folder = input("Enter path to your movies folder: ").strip()
    if not os.path.isdir(folder):
        print("Invalid folder path.")
    else:
        process_directory(folder)
