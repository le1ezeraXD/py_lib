#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import sys
import pandas as pd

# 不会创建record的测项 以及record.csv中特有的测项
dummy_item = {'End','DRCB_OverallResult','Transition_BootArgs_Set_Astro_BMC','Version','Group','QuerySFC_SBin_BMC'}


def main():

    # 传入record.csv and main.csv
    # 以文件形式保存
    record_csv = "/Users/device/Downloads/JXYCM9TYGD/20250210_22-40-41.041-315851/system/records.csv"
    main_csv = "/Users/device/Desktop/MainTable.csv"
    # record_csv = input("传入record.csv: \n").strip()
    # main_csv = input("传入MainTable.csv: \n").strip()
    SystemType = "FULL"
    FanType = "SanAce"
    # SystemType = input("设置SystemType(FULL/BASE): \n").upper()
    # if SystemType not in ["FULL","BASE"]:
    #     print("SystemType格式设置有误")
    #     sys.exit()
    # FanType = input("设置FanType(FX/SanAce)区分大小写: \n")
    # if FanType not in ["FX","SanAce"]:
    #     print("FanType格式设置有误, 请注意区分大小写")
    #     sys.exit()

    # 使用set去重
    record_test_item = set()
    main_test_item = set()

    # 处理有condition的测项
    # 如: 当前SystemType为FUll
    # 那么Compare_OS_Version_BASE就忽略不计
    # FanType同理
    SystemType = "FULL" if SystemType == "BASE" else "BASE"
    FanType = "FX" if FanType == "SanAce" else "SanAce"

    # 尝试读取整个csv 然后逐行拼接 方便处理Atlas项的问题
    # 处理Main.csv
    try:
        with open(main_csv, mode='r', encoding='utf-8') as csv_file:
            # 以字典格式读取csv
            reader = csv.DictReader(csv_file)
            for row in reader:
                # 对于MainTable来说 测项名为Coverage与TestParameters拼接 如果TestParameters为空则不拼
                item = row['Coverage'] + (("_" + row['TestParameters']) if row['TestParameters'] else "")
                # 处理多线程以及Teardown分割行
                if item not in ['-_-','=_=']:
                    # 同前面处理condition测项
                    if not item.endswith((SystemType, FanType)):
                        main_test_item.add(item)
    except FileNotFoundError:
        print(f"{main_csv} 文件不存在!")
    except pd.errors.EmptyDataError:
        print(f"{main_csv} 文件为空!")
    except Exception as e:
        print("未知错误")


    try:
        # 处理record.csv
        # 与main同
        with open(record_csv, mode='r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                item = row['subTestName']
                if item and not item.startswith(("c0","c1")):
                    # print(item)
                    if not item.endswith((SystemType, FanType)):
                        record_test_item.add(item)
    except FileNotFoundError:
        print(f"{record_csv} 文件不存在!")
    except pd.errors.EmptyDataError:
        print(f"{record_csv} 文件为空!")
    except Exception as e:
        print("未知错误")


    # print(len(main_test_item))
    # print(len(record_test_item))
    cnt = 0
    # 检查两个csv中record是否有遗漏
    # 除了一些不会create record的测项 已写在前面dummy_item中
    for item in main_test_item:
        if item not in record_test_item:
            if item in dummy_item or item.find('WaitFor') > -1: continue
            print(item)
            cnt += 1

    for item in record_test_item:
        if item not in main_test_item:
            if item in dummy_item or item.find('WaitFor') > -1: continue
            print(item)
            cnt += 1

    if cnt > 0:
        print("Some item error")
    else:
        print("PASS!!")


if __name__ == "__main__":
    main()