import os

base_path = (input("the base path of scripts>>>")).strip('"').strip()
output_path = os.path.join(base_path, "Bomout")
os.makedirs(output_path, exist_ok=True) # 无输出

def get_f(f_path):
    # 获取文件夹中文件的绝对路径
    f_ls = [os.path.abspath(os.path.join(f_path, f)) for f in os.listdir(f_path)]
    return f_ls

def convert2utf16leWithBom(text_ls):
    for text in text_ls:
        if os.path.isfile(text):
            try:
                with open(text, "r", encoding="utf-16le") as f:
                    content = f.read()

                # 写入带有 BOM 的 UTF-16LE 文件
                e = os.path.basename(text)

                with open(f"{output_path}/{e}", "w", encoding="utf-16le") as f2:
                    f2.write('\ufeff')
                    f2.write(content)

                print(f"adding bom to {text} in UTF-16LE ")

            except Exception as e:
                print(f"Failed to convert {text}: {e}")

convert2utf16leWithBom(get_f(base_path))
