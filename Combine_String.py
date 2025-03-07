import os
import re

# 与add_Tech_Coverage.py配合使用 效果更佳
# 注: 以下情况会有bug尚未修复 需手动检查
#   一条字符串拼接两个变量 如: [[syscfg add SILC 0x50003 0x0 0x]] .. amber_postCal_syscfg_pwmHex_global .. white_postCal_syscfg_pwmHex_global .. [[ 0x0 0x0 0x0 0x0]],
#   两条字符串中间拼接的并非变量 而是某转义字符 如: [[SPK mic in position?]] .. '\n' .. [[治具SPK是否推到定位？]],
#   以上属于少数情况 故未做针对性调整

def transform_lua_content(ss):

    # 先写好原先字符串拼接可能的格式
    text1 = r"\[\[(.*?)\]\] .. (.*) .. \[\[(.*)\]\] .. (.*) .. \[\[(.*)\]\]"
    text2 = r"\[\[(.*?)\]\] .. (.*) .. \[\[(.*)\]\] .. (.*)"
    text3 = r"\[\[(.*?)\]\] .. (.*) .. \[\[(.*)\]\]"
    text4 = r"\[\[(.*?)\]\] .. (.*),"

    # 使用pattern抓取字符串拼接时[[]]内的内容和拼接的变量
    # 使用while的原因：
    #   由于同一文件中可能存在多个拼接格式相同的字符串 如:
    #   [[Test1]] .. Variable1,
    #   [[Test2]] .. Variable2,
    #   此时如果统一替换, Test2 Variable2都会被替换成Test1 Variable1
    #   所以在re.sub中限制每次只替换一次, 同时使用search做循环条件
    #   当文件中找不到当前拼接格式的字符串, 即所有字符串都替换完毕, 跳出循环
    pattern1 = re.compile(text1)
    while pattern1.search(ss):
        # 根据String.cFormatString的格式进行重新拼接
        cFormatString1 = f"""String.cFormatString("{pattern1.search(ss).group(1)}%s{pattern1.search(ss).group(3)}%s{pattern1.search(ss).group(5)}",{{{pattern1.search(ss).group(2)},{pattern1.search(ss).group(4)}}}),"""
        ss = re.sub(text1,cFormatString1,ss,1)

    pattern2 = re.compile(text2)
    while pattern2.search(ss):
        cFormatString2 = f"""String.cFormatString("{pattern2.search(ss).group(1)}%s{pattern2.search(ss).group(3)}%s",{{{pattern2.search(ss).group(2)},{pattern2.search(ss).group(4)}}}),"""
        ss = re.sub(text2,cFormatString2,ss,1)

    pattern3 = re.compile(text3)
    while pattern3.search(ss):
        cFormatString3 = f"""String.cFormatString("{pattern3.search(ss).group(1)}%s{pattern3.search(ss).group(3)}",{{{pattern3.search(ss).group(2)}}}),"""
        ss = re.sub(text3,cFormatString3,ss,1)

    pattern4 = re.compile(text4)
    while pattern4.search(ss):
        cFormatString4 = f"""String.cFormatString("{pattern4.search(ss).group(1)}%s",{{{pattern4.search(ss).group(2)}}}),"""
        ss = re.sub(text4,cFormatString4,ss,1)

    return ss


def Combine_String(root_dir):
    for root, dirs, files in os.walk(root_dir):
        first_level_dir = os.path.basename(root)

        for file in files:
            # 检查是否lua文件
            if file.endswith(".lua"):
                file_path = os.path.join(root, file)

                # 读取文件内容
                with open(file_path, "r") as f:
                    content = transform_lua_content(f.read())

                with open(file_path, "w") as f:
                    f.write(content)

Combine_String("/Users/device/Desktop/de_Aim_Bot")