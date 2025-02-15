#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import os.path
import sys
import pandas as pd

# 不会创建record的测项 以及record.csv中特有的测项
dummy_item = {'End','DRCB_OverallResult','Transition_BootArgs_Set_Astro_BMC','Version','Group','QuerySFC_SBin_BMC'}


def main():

    # 传入record.csv and main.csv
    # 以文件形式保存
    # 检查文件是否存在
    record_csv = input("传入record.csv: \n").strip()
    record_csv = record_csv.replace('\ ',' ')
    if not os.path.exists(record_csv):
        print(f"{record_csv} 路径有误或文件不存在!")
        sys.exit()

    main_csv = input("传入MainTable.csv: \n").strip()
    main_csv = main_csv.replace('\ ', ' ')
    if not os.path.exists(main_csv):
        print(f"{main_csv} 路径有误或文件不存在!")
        sys.exit()

    SystemType = input("设置SystemType(FULL/BASE)不区分大小写: \n").upper()
    if SystemType not in ["FULL","BASE"]:
        print("SystemType格式设置有误")
        sys.exit()
    FanType = input("设置FanType(FX/SanAce)不区分大小写: \n").lower()
    if FanType not in ["fx","sanace"]:
        print("FanType格式设置有误")
        sys.exit()

    # 使用set去重
    record_test_item = set()
    main_test_item = set()

    # 处理有condition的测项
    # 如: 当前SystemType为FUll
    # 那么Compare_OS_Version_BASE就忽略不计
    # FanType同理
    SystemType = "FULL" if SystemType == "BASE" else "BASE"
    FanType = "FX" if FanType == "sanace" else "SanAce"

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
        sys.exit()
    except pd.errors.EmptyDataError:
        print(f"{main_csv} 文件为空!")
        sys.exit()


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
        sys.exit()
    except pd.errors.EmptyDataError:
        print(f"{record_csv} 文件为空!")
        sys.exit()

    print("\n\n========================================\n")
    cnt_Main = 0
    # 检查两个csv中record是否有遗漏
    # 除了一些不会create record的测项 已写在前面dummy_item中
    for item in main_test_item:
        if item not in record_test_item:
            if item in dummy_item or item.find('WaitFor') > -1: continue
            if cnt_Main == 0: print("不在record.csv中的Main测项为:")
            print(item)
            cnt_Main += 1

    cnt_Record = 0
    for item in record_test_item:
        if item not in main_test_item:
            if item in dummy_item or item.find('WaitFor') > -1: continue
            if cnt_Record == 0: print("不在MainTable.csv中的Record为:")
            print(item)
            cnt_Record += 1

    if cnt_Main == 0: print("无Main测项缺失!!!")
    else: print(f"Main有{cnt_Main}项缺失!!!")
    if cnt_Record == 0: print("无Record测项缺失!!!")
    else:print(f"Record.csv有{cnt_Record}项缺失!!!")
    print("\n=========================================")
    if cnt_Main + cnt_Record == 0: print("无测项缺失!!!")


if __name__ == "__main__":
    main()