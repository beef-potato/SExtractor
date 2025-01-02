import os
"""
这个脚本接受一个目录的绝对路径，遍历所有该目录下的文本文件（当前未写类型判断，只是遍历所有非文件夹类型的文件），
所以应该保持这个 folder 下除了 child folder 以外都是 text file.

用 cp932 打开文本文件，然后用 utf-16 le bom 保存。

"""
base_path = (input("the base path of scripts>>>")).strip('"').strip()
output_path = os.path.join(base_path, "utf16leBom")
os.makedirs(output_path, exist_ok=True) # 在 out_path 里输出结果，如果没有的话就不输出。

def get_f(f_path):
    # 获取文件夹中文件的绝对路径
    f_ls = [os.path.abspath(os.path.join(f_path, f)) for f in os.listdir(f_path)]
    return f_ls

def convert2utf16le(text_ls):
    for text in text_ls:
        if os.path.isfile(text):
            try:
                with open(text, "r", encoding="cp932") as f:
                    content = f.read()

                # 写入带有 BOM 的 UTF-16LE 文件
                e = os.path.basename(text)
                with open(f"{output_path}/{e}", "w", encoding="utf-16le") as f2:
                    f2.write('\ufeff')
                    f2.write(content)

                print(f"Converted {text} to UTF-16LE with bom")

            except Exception as e:
                print(f"Failed to convert {text}: {e}")

convert2utf16le(get_f(base_path))

# f2.write('\ufeff') : https://stackoverflow.com/questions/5202648/adding-bom-unicode-signature-while-saving-file-in-python


