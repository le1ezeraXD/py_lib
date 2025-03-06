import os

# 用于在action lua开头处写入行
# 适用tag, require等

def add_comment_to_action_lua(root_dir):
    for root, dirs, files in os.walk(root_dir):
        first_level_dir = os.path.basename(root)

        for file in files:
            # 检查是否lua文件
            if file.endswith(".lua"):
                file_path = os.path.join(root, file)

                # 读取文件内容
                with open(file_path, "r") as f:
                    content = f.read()

                    coverage = str(file).replace(".lua","")
                    # 构造注释行
                    # comment_line = f"-- {first_level_dir},{coverage}\n"

                    # 构造require行
                    comment_line = """local String = require("FXModules/FXLuaFunc/Common/String")\n"""

                    #写入行
                    if comment_line not in content:
                        with open(file_path, "w") as f:
                            f.write(comment_line+content)
                        print(comment_line)

root_dir = "/Users/device/Desktop/de_Aim_Bot/"
add_comment_to_action_lua(root_dir)
