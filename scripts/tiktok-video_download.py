#!/usr/bin/env python3

# Copyright (C) 2025 qvipin
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import json
import urllib.request as download
import urllib.error as download_error
import http.client as download_error2
import os, sys

if len(sys.argv) > 1:
    json_file = sys.argv[1]
else:
    print("Usage: ./tiktok-video_download.py <JSON File>")
    sys.exit(1)

"""JSON File"""
if not json_file.endswith(".json"):
    print("[*] Error: File not JSON, please specify a valid Tiktok User Data JSON file")
    sys.exit(1)

try: 
    with open(json_file, 'r') as file: 
        user_data_tiktok = file.read()
except (FileNotFoundError, IsADirectoryError): 
    print("[*] File Not Found, quitting the program...")
    sys.exit(1)


"""JSON Parsing"""
data = json.loads(user_data_tiktok)

video_list = data["Video"]["Videos"]["VideoList"]

"""Downloading the files"""

os.makedirs("./Tiktok_Videos", exist_ok=True)

def vid_name_gen(video_url, vid_date): # Gives the correct file extension for the file
    if "jpeg" in video_url: # ensuring the file isnt a jpeg and messing up the download
        vid_name = vid_date + ".jpeg" 
    else: 
        vid_name = vid_date + ".mp4" 
    return vid_name

def file_path_from_name(vid_name): # Deriving file path from name
    folder_name = "./Tiktok_Videos"
    file_path = os.path.join(folder_name, vid_name)
    return file_path



for item in range(0, len(video_list)):
    try:
        vid_date = ((video_list[item]['Date']).replace(" ", "_")).replace(":", "-") # name & date
        video_url = video_list[item]['Link']             
        
        vid_name = vid_name_gen(video_url, vid_date) 
        
        file_path = file_path_from_name(vid_name)
        
        download.urlretrieve(video_url, file_path)
        print(f"[*] Downloading: {vid_name}, currently on item {item}/{len(video_list)}")
    except (download_error.HTTPError, download_error2.InvalidURL, download_error.URLError, ValueError):
        # the code below checks for newlines in url as that is how slideshow image links are represented, so we need to download them in a different way
        if "\n" in video_url: 
            urls = video_url.strip().split("\n")
            for url in urls:
                try:
                    vid_name = vid_name_gen(url, vid_date) 
        
                    file_path = file_path_from_name(vid_name)
                    
                    download.urlretrieve(url, file_path)
                    print(f"[*] Downloading: {vid_name}, currently on item {item}/{len(video_list)}")
                except (download_error.HTTPError, download_error2.InvalidURL, download_error.URLError, ValueError):
                    print(f"[*] Oops, we can't download a part of {item}/{len(video_list)}! (FYI: This item is a slideshow.)")

        else:
            print(f"[*] Oops, we can't download item {item}/{len(video_list)}!")
            continue
    except KeyboardInterrupt:
        print("[*] CTRL + C Detected, quitting the program...")

print("[*] Done! Go check the Tiktok_Videos folder for your videos!")