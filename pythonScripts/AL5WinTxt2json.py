import re
import json

# text_pattern = re.pattern("#1-TEXT\n\[(\s)\]")
# not completed

def read_txt(f_path):
    sentences = []

    with open(f_path, 'r', encoding='shift-jis') as f:
        txt_content = f.readlines()
    for line in txt_content:
        if "TEXT" in line and "SYSTEM" not in line:
            sentences.append(line)

    return sentences

def convert2json(raw_list):
    json_ls = []
    for i in range(len(raw_list)):
        temp_dict = {"message": f"{raw_list[i]}"}
        json_ls.append(temp_dict)
    
    res = json.dumps(json_ls)
    # print(res)
    return res 


def saveRes(json_string:str, f_path):
    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(json_string)



if __name__ == "__main__":
    test_f = "../elfDatsui_txt/AA_H1.txt"
    out_file = "../elfDatsui_json/AA_H1.json"

    result = read_txt(test_f)
    print(result)
    # res = convert2json(test_f)
    # saveRes(res)

    pass


