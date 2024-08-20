"""将字典中的所有分隔符变成tab"""

import os
import re

blank_pattern = r"[ \t]+"
folder_path = input("Enter the folder of the project >> ").strip()

def replace_with_tab(f_path: str):
    input_file = os.path.join(f_path, "项目GPT字典.txt")
    output_file = os.path.join(f_path, "项目GPT字典2.txt")
    
    with open(input_file, 'r', encoding="utf-8") as f:
        project_dict = f.readlines()
    
    res_ls = []
    for line in project_dict:
        # Replace all sequences of whitespace with a single tab
        temp_ls = [e for e in line.split()]
        temp_line = "\t".join(temp_ls)+"\n"
        res_ls.append(temp_line)
    
    with open(output_file, "w", encoding="utf-8") as f2:
        f2.writelines(res_ls)

replace_with_tab(folder_path)
