# -*- coding: utf8 -*-

Encry_ti = 0  # 加密次数（加密字符串长度）
enc = ''  # 密文


def Slow_rot(input_str):
    global Encry_ti
    init_list_left = [x for x in range(1, 27)]  # 创建初始表
    for i in range(3):
        item = init_list_left.pop()
        init_list_left.insert(0, item)
    init_list_right = [21, 3, 15, 1, 19, 10, 14, 26, 20, 8,
                       16, 7, 22, 4, 11, 5, 17, 9, 12, 23, 18, 2, 25, 6, 24, 13]  # 创建初始表
    if Encry_ti % 676 == 0 and Encry_ti != 0:  # 若中转子和快转子都转了一周后满转子转一次
        item = init_list_left.pop()
        init_list_left.insert(0, item)
        item = init_list_right.pop()
        init_list_right.insert(0, item)
    first_ind = ord(input_str)-65  # 将大写字母由ASCII码转化到index
    return init_list_right.index(init_list_left[first_ind])


def Med_rot(input_num):
    global Encry_ti
    init_list_left = [x for x in range(1, 27)]  # 创建初始表
    for i in range(1):
        item = init_list_left.pop()
        init_list_left.insert(0, item)
    init_list_right = [20, 1, 6, 4, 15, 3, 14, 12, 23, 5, 16,
                       2, 22, 19, 11, 18, 25, 24, 13, 7, 10, 8, 21, 9, 26, 17]  # 创建初始表
    if Encry_ti % 26 == 0 and Encry_ti != 0:  # 若快转子转了一周后中转子转一下
        item = init_list_left.pop()
        init_list_left.insert(0, item)
        item = init_list_right.pop()
        init_list_right.insert(0, item)
    return init_list_right.index(init_list_left[input_num])


def Fas_rot(input_num):
    global Encry_ti
    init_list_left = [x for x in range(1, 27)]  # 创建初始表
    init_list_right = [8, 18, 26, 17, 20, 22, 10, 3, 13, 11,
                       4, 23, 5, 24, 9, 12, 25, 16, 19, 6, 15, 21, 2, 7, 1, 14]  # 创建初始表
    if Encry_ti != 0:  # 每加密一个字母便转一下
        for i in range(Encry_ti):
            item = init_list_left.pop()
            init_list_left.insert(0, item)
            item = init_list_right.pop()
            init_list_right.insert(0, item)
    ind = init_list_right.index(init_list_left[input_num])  # 由index转化到字母index
    return chr(ind+65)


def encry(input_str):
    return Fas_rot(Med_rot(Slow_rot(input_str)))  # 经过三个转子后输出加密后字母


text = input("Please enter the text to be encrypted:")
if text.isupper():  # 检查输入
    str_len = len(text)
    for i in range(str_len):
        enc, Encry_ti
        Encry_ti = i
        enc += encry(text[i])
else:
    print("Input can only be capital letters!!")

print("After encryption:", enc)
