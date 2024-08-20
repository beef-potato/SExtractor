"""
移除ks脚本中的非必要方括号控制语句
默认编码：utf-16 le

"""
import re
import os

folder_path = r"D:\code\python\GalTransl\hime\gameText"

SBracketsPattern = r"\[.*?\]"

"""
[※]鋼の意志を持つ男…それがこの俺、[f t=まき]巻[f t=しん]信[f t=た]太[f t=ろう]郎だ…くくく。

[※][big2]なんじゃこりゃぁあああ…！！

[男]「あぁ？なんだてめぇ…[setQuake t=600 se="殴る：ドゴォ" wq=false]ガァァ！！？」

[きよら][big2]「その下品な男の本能を抑え込めなかった信太郎の不甲斐なさに対してよぉぉぉ！！」

"""


def get_files(f_path):
    file_ls = []
    for f in os.listdir(f_path):
        f = os.path.join(f_path, f)  # Join the folder path with the file name
        if os.path.isfile(f):
            file_ls.append(os.path.abspath(f))  # Get absolute path
    return file_ls


def find_SB(file_ls):
    sb_set = set()
    for f in file_ls:    
        with open(f, 'r', encoding="utf-16le") as tempf:
            content = tempf.readlines()
            for line in content:
                matches = re.findall(SBracketsPattern, line)
                for match in matches:  # Loop through each match and add to the set
                    sb_set.add(match)
    return sb_set


# print(find_SB(get_files(folder_path)))

# file_ls = get_files(folder_path)
# for e in find_SB(file_ls=file_ls):
#     print(e)
# 种类很多，大量纯日文控制字符 



