import csv


# 定义一个函数来返回带有序号后缀的字符串
# def get_ordinal_suffix(n):
#     if 10 <= n % 100 <= 20:
#         suffix = 'th'
#     else:
#         suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
#     return f'{n}{suffix}'


# 统一的 test Parameters 参数前缀
unified_test_param = "Unified Test Parameter"
limit_set = set()
main_set = set()

# 读取原始CSV文件
with open('limit_test.csv', mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)  # 将原始CSV的内容读取到列表中
    for row in rows:
        sb = row["Coverage"] + row["TestParameters"]
        limit_set.add(sb)

with open('main_test.csv', mode='r', newline='', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)  # 将原始CSV的内容读取到列表中
    for row in rows:
        sb = row["Coverage"] + row["TestParameters"]
        main_set.add(sb)


for sb in limit_set:
    if sb not in main_set:
        print(sb)

# 创建一个新的列表来存储复制后的数据
new_rows = []

# 复制并生成新的 test Parameters
# for i in range(1, 201):  # 复制200次
#     for row in rows:
#         ordinal = get_ordinal_suffix(i)  # 根据复制次数生成序号后缀
#         new_row = row.copy()  # 复制当前行，防止修改原始行
#         new_row['TestParameters'] = f"{new_row['TestParameters']}_{ordinal}"  # 更新 test Parameters 列
#         new_rows.append(new_row)  # 将新的行添加到新的列表中
#         print(new_row)
#
# # 写入新的CSV文件
# with open('updated_file.csv', mode='w', newline='', encoding='utf-8') as outfile:
#     fieldnames = reader.fieldnames  # 获取原始CSV中的列名
#     writer = csv.DictWriter(outfile, fieldnames=fieldnames)
#
#     writer.writeheader()  # 写入列名
#     writer.writerows(new_rows)  # 写入所有复制后的行