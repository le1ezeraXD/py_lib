# O(n)复杂度检测数组中是否有重复数字
# 第一种方法: 排序后遍历 时间复杂度为O(nlogn + n)
# 第二种方法: 使用一个长度为n的哈希表或数组 时间复杂度为O(n) 代价是一个空间O(n)的哈希表或数组 属于空间换时间
# 最优解: 遍历数组 当扫描下标为i的数字时(记为m) 先将它与i做比较 如果是则继续比较
# 如果不是则将它与下标m的数字做比较 如果相等证明重复 如果不等则将它与下标m的数字交换位置
import random

arr = [2,3,1,0,2,5,3]

def repeat_num_exist(arr):
    for i in range(0,len(arr)):
        m = arr[i]
        if m != i:
            if m == arr[m]:
                print(f"repeating digs is {m}")
            else:
                arr[i], arr[m] = arr[m], arr[i]


# 九宫 = [
#     [2,9,4],
#     [7,5,3],
#     [6,1,8],
# ]


# 二维数组查找数字
# 从左到右递增 从上到下递增
# 解法：从右上角开始做比较
# 如果右上角数字等于target直接返回，如果大于则删除这一列，如果小于则删除这一行
# 中心思想为根据递增的规律逐渐缩小查找范围 直到找到为止

def find(matrix, target):
    found = False
    rows = len(matrix)
    columns = len(matrix[0])
    if matrix and rows > 0 and columns > 0:
        row, column = 0, columns-1
        while row < rows and column >= 0:
            if matrix[row][column] == target:
                found = True
                break
            elif matrix[row][column] > target:
                column -= 1
            else:
                row += 1

    return found

Two_dimensional_array = [
    [1,2,8,9],
    [2,4,9,12],
    [4,7,10,13],
    [6,8,11,15],
]

# if find(Two_dimensional_array, 1):
#     print("Find!")
# else:
#     print("SB!")

# 斐波那契数列
# 时间复杂度O(n)的做法
# 不用递归: 开销太大 且重复计算很多
# 青蛙跳台阶: 一次跳1 一次跳2
# n>2时 如果跳1 此时跳法数目为f(n-1); 如果跳2 此时跳法数目为f(n-2)
# 即为斐波那契数列

def Fibonacci(n):
    if n < 2: return n
    fibOne = 1
    fibTwo = 0
    fibSum = 0
    for i in range(2,n+1):
        fibSum = fibOne + fibTwo
        fibTwo = fibOne
        fibOne = fibSum

    return fibSum

def Fibonacci_recursive(n):
    if n < 2: return n
    return Fibonacci_recursive(n-1) + Fibonacci_recursive(n-2)


# Quick Sort

def Partition(data,start,end):
    if not data or start < 0 or end >= len(data):
        print("Invalid Input")

    index = random.randint(start,end)
    data[index],data[end] = data[end],data[index]

    small = start-1
    for i in range(start,end):
        if data[i] < data[end]:
            small += 1
            if small != i:
                data[i], data[small] = data[small], data[i]

    small += 1
    data[small], data[end] = data[end], data[small]

    return small

def QuickSort(data,start,end):
    if start == end:
        return
    index = Partition(data,start,end)
    if index > start: QuickSort(data,start,index-1)
    if index < end: QuickSort(data,index+1,end)


arr_unsorted = [2,3,1,0,2,5,3]
QuickSort(arr_unsorted,0,len(arr_unsorted)-1)
print(arr_unsorted)