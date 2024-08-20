import os

folder_path = r"D:\code\python\GalTransl\hime\backup"


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
                with open(f"{folder_path}/../py_utf16le_noBOM/{e}", "w", encoding="utf-16le") as f2:
                    f2.write(content)

                print(f"Converted {text} to UTF-16LE without bom")

            except Exception as e:
                print(f"Failed to convert {text}: {e}")

convert2utf16le(get_f(folder_path))

# 看来必须是有签名的版本才行，单纯的 encoding="utf-16le"是无签名的版本，会黑屏；也许teakadanshi也是这个问题。
# shift_jisx0213 支持更多日文字符 / cp932?
# f2.write(codecs.BOM_UTF16_LE) 有签名的utf-16le 版本
# 再次失败了，就算有签名，似乎因为这个签名导致控制序列出现问题了。
# 有可能文本本身存在什么头序列?
# 直接用emeditor转换为有签名的utf-16le, 则可以被游戏文本读取，同样是有签名的utf-16le,到底有什么区别？
# 脚本生成的文件直接黑屏，就算用了codecs 不会报错，也无法读取。
# 如果使用vscode打开脚本，则会发现codecs生成的文本是二进制文本，虽然emeditor可以读取，vscode 则不行。
# 这或许说明最简单的方式就是直接用emeditor先转码所有的文本文件，然后用python提取文本，按照原来的格式读取，如果这样可以的话也算是可行的，希望
# python 保存的时候不要修改文件头部信息。
# f2.write('\ufeff') : https://stackoverflow.com/questions/5202648/adding-bom-unicode-signature-while-saving-file-in-python
# 没想到上面这个居然可以，果然是文件头的问题，codecs因为添加的是二进制的文件头，所以无法被读取。


