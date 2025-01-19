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
import sys

if len(sys.argv) > 1:
    json_file = sys.argv[1]
else:
    print("Usage: ./tiktok-comments_save.py <JSON File>")
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

"""Comments File"""
comment_file = open("./comments.txt", 'w') 

    
"""JSON Parsing"""

data = json.loads(user_data_tiktok)

comment_list = data["Comment"]["Comments"]["CommentsList"]

for comment in range(0, len(comment_list)):
    try: 
        comment_date = comment_list[comment]['date']
        comment_content = comment_list[comment]['comment']             
        comment_file.write(f"{comment_date}: {comment_content}\n")
        print(f"[*] Saving your comments to comments.txt. {str(int(comment)/int(len(comment_list)))[2:4]}% done")
    except KeyboardInterrupt:
        print("[*] CTRL + C Detected, quitting the program...")


comment_file.close()
print(f"[*] Done! Go check the comments.txt file for all your {len(comment_list)} comments!")