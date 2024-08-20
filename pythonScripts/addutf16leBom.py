import os

folder_path = r"D:\galgame\teakaDanshi\patch02"
base_path = r"D:\galgame\teakaDanshi"

def get_f(f_path):
    # 获取文件夹中文件的绝对路径
    f_ls = [os.path.abspath(os.path.join(f_path, f)) for f in os.listdir(f_path)]
    return f_ls

def convert2utf16le(text_ls):
    for text in text_ls:
        if os.path.isfile(text):
            try:
                with open(text, "r", encoding="utf-16le") as f:
                    content = f.read()

                # 写入带有 BOM 的 UTF-16LE 文件
                e = os.path.basename(text)

                with open(f"{base_path}/patch/{e}", "w", encoding="utf-16le") as f2:
                    f2.write('\ufeff')
                    f2.write(content)

                print(f"adding bom to {text} in UTF-16LE ")

            except Exception as e:
                print(f"Failed to convert {text}: {e}")

convert2utf16le(get_f(folder_path))


