import os
import json

"""

encode: utf-8

[
  {
    "name": "i n=教官",
    "message": "「……と、いうことで。各自、己の目的を忘れぬよう責務を果たし」"
  },
  {
    "name": "i n=教官",
    "message": "「主にその全てを捧げ、尽くし、守り、仕える事を誓いますか？」"
  },

  ]

"""


read_rate = 2  # lines per second
folder_path = input("the json folder>>>").strip().strip('"')
folder_path = os.path.abspath(folder_path)

def get_lines(f_path):
    json_ls = os.listdir(f_path)
    line_count = 0
    for json_f in json_ls:
        full_path = os.path.join(f_path, json_f)
        with open(full_path, 'r', encoding="utf-8") as f:
            data = json.load(f)
        # Count all lines in the "message" fields
        message_count = sum(len(item['message'].split('\n')) for item in data)
        line_count += message_count
    return line_count

def calculate_time(line_num):
    time_in_s = line_num / read_rate
    time_in_hours = time_in_s / 60 / 60
    print(f'The total time will be around {time_in_hours:.2f} hours')

calculate_time(get_lines(folder_path))










