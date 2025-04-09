import os
import re
import shutil

def copy_EFICmd_Test(source_folder, target_folder):
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.lua'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if 'sendEFICmd' in content:
                            # 获取相对于源目录的路径
                            rel_path = os.path.relpath(file_path, source_folder)
                            rel_parts = rel_path.split(os.sep)

                            # 只保留最后两个部分路径（倒数两级文件夹）
                            if len(rel_parts) >= 2:
                                partial_path = os.path.join(rel_parts[-2], rel_parts[-1])
                            else:
                                partial_path = rel_parts[-1]

                            # 构造目标完整路径
                            dest_path = os.path.join(target_folder, partial_path)

                            # 创建中间目录（如果不存在）
                            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                            # 执行复制
                            shutil.copyfile(file_path, dest_path)
                            print(f"已复制: {file_path} -> {dest_path}")
                except Exception as e:
                    print(f"无法读取文件 {file_path}，错误: {e}")

# 源文件夹和目标文件夹路径
source_folder = r'/Users/device/Desktop/de_Aim_Bot'  # 替换为你放lua文件的路径
target_folder = r'/Users/device/Desktop/EFICmd_Training'  # 替换为你想复制到的路径

# 如果目标文件夹不存在，就创建它
os.makedirs(target_folder, exist_ok=True)

# copy_EFICmd_Test(source_folder, target_folder)

def lua_pattern_to_regex(lua_pattern: str) -> str:
    """
    将 Lua 字符串模式转换为 Python 正则表达式。
    注意：这是一个简化版本，仅适用于常见模式。
    """
    # 映射表：Lua 转正则
    conversions = {
        '%a': '[A-Za-z]',
        '%A': '[^A-Za-z]',
        '%d': r'\d',
        '%D': r'\D',
        '%w': r'\w',
        '%W': r'\W',
        '%s': r'\s',
        '%S': r'\S',
        '%x': '[0-9A-Fa-f]',
        '%p': r'[!\"#$%&\'()*+,\-./:;<=>?@[\\\]^_`{|}~]',
        '%c': '',  # 控制字符暂不处理
        '%.': r'\.',  # 转义的点
        '%[': r'\[',
        '%]': r'\]',
        '%^': r'\^',
        '%$': r'\$',
        '%*': r'\*',
        '%+': r'\+',
        '%-': r'\-',
        '%(': r'\(',
        '%)': r'\)',
    }

    # 逐字符解析
    i = 0
    regex = ''
    while i < len(lua_pattern):
        c = lua_pattern[i]

        # Lua 的转义符
        if c == '%' and i + 1 < len(lua_pattern):
            token = lua_pattern[i:i+2]
            regex += conversions.get(token, re.escape(token))
            i += 2
        elif c in {'.', '^', '$', '*', '+', '-', '?', '(', ')', '[', ']', '{', '}', '|', '\\'}:
            # 需要转义的正则符号（非 Lua 特定）
            regex += '\\' + c
            i += 1
        else:
            regex += c
            i += 1

    # 替换 Lua 的 `-`（非贪婪）为正则的 `*?`
    regex = re.sub(r'(\.|\\w|\\d|\[.*?\])\-', r'\1*?', regex)

    return regex


FBAD = "FBAD = testFBAD123\tOK"
pattern = "FBAD =\s*(.+?)\s*[\r\n\t]+OK"
print(re.search(pattern,FBAD).group(1))