import os
import re

blank_pattern = r"[ \t]{2,}"
def replace_with_tab(f_path: str):
    input_file = os.path.join(f_path, "项目GPT字典.txt")
    output_file = os.path.join(f_path, "项目GPT字典2.txt")
    
    with open(input_file, 'r', encoding="utf-8") as f:
        project_dict = f.readlines()
    
    res_ls = []
    for line in project_dict:
        # Print original line for debugging
        print(f"Original: {repr(line)}")
        # Replace all sequences of spaces or tabs with a single tab
        temp_line = re.sub(blank_pattern, "\t", line)
        # Print modified line for debugging
        print(f"Modified: {repr(temp_line)}\n")
        res_ls.append(temp_line)
    
    with open(output_file, "w", encoding="utf-8") as f2:
        f2.writelines(res_ls)

replace_with_tab("DanshiProject")
