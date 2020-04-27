# -*- coding: utf8 -*-
# 参照https://github.com/RobinDavid/pydes/blob/c6a1f909569cd2d19568709ad1da3a62ccb5d2cf/pydes.py


# 初始置换PI
PI = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# 子密钥生成时首先进行的置换PC_1
PC_1 = [57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4]

# 每次循环左移后生成的该轮的子密钥前进行的置换
PC_2 = [14, 17, 11, 24, 1, 5, 3, 28,
        15, 6, 21, 10, 23, 19, 12, 4,
        26, 8, 16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55, 30, 40,
        51, 45, 33, 48, 44, 49, 39, 56,
        34, 53, 46, 42, 50, 36, 29, 32]

# 每轮迭代中的选择扩展运算，从32bit扩展到48bit
E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

# SBOX 从48bit压缩到32bit，通过8个选择函数组每个函数组从6bit到4bit
S_BOX = [

    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
     ],

    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
     ],

    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
     ],

    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
     ],

    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
     ],

    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
     ],

    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
     ],

    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
     ]
]

# 经过S-box压缩后进行P置换
P = [16, 7, 20, 21, 29, 12, 28, 17,
     1, 15, 23, 26, 5, 18, 31, 10,
     2, 8, 24, 14, 32, 27, 3, 9,
     19, 13, 30, 6, 22, 11, 4, 25]

# 16轮迭代完后进行逆初始置换PI_1
PI_1 = [40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25]

# 每轮密钥进行循环左移时的位数
SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


def string_to_bits(string):  # 将字符串变为bit串
    bits = []
    for i in string:
        bits.extend([int(x) for x in binval(i, 8)])  # 8 bits in a group
    return bits  # 形如[0,0,1,1,···]的list，长度为字符串长度*8


def binval(str, lenth):  # 将一个字符变为8bit
    binvalue = bin(str)[2:] if isinstance(str, int) else bin(ord(str))[2:]
    if len(binvalue) > lenth:
        raise "The character cannot be converted to 8 bits"
    while len(binvalue) < lenth:
        binvalue = "0" + binvalue
    return binvalue  # 返回形如'00110001'的字符串


def bits_to_string(bits):  # 将bit串转化为字符串，相当于string_to_bits的逆函数
    output = ''
    li = split(bits, 8)
    for i in li:
        output += chr(int(''.join([str(x) for x in i]), 2))
    return output


def split(list, n):  # 将原list变为含8个元素为一个子list的list
    # 形如[[0,1,1,···],[1,1,0,···]]
    return [list[k:k+n] for k in range(0, len(list), n)]


class DES():
    def __init__(self):
        self.key = None
        self.text = None
        self.round_keys = []

    def run(self, key, text, action):
        if len(key) < 8:
            raise "It is too short! Key should be 8 bytes long"
        elif len(key) > 8:
            raise "It is too long! Key should be 8 bytes long"
        self.key = key
        self.text = text
        self.key_gener()  # 生成子密钥
        blocks = split(self.text, 8)  # 将输入分为8个字符为一个元素的list
        output = []
        for block in blocks:  # 依次对每8个字符进行加密
            # 将单个字符转到8个bit，8个字符一组便是64个bit，block为64个int型数据的list
            block = string_to_bits(block)
            # 16轮迭代之前的初始置换PI，left与right均为32个int型元素的list
            left, right = split(self.substi(block, PI), 32)
            for i in range(16):  # 16轮循环
                temp = self.expend(right, E)  # 选择扩展运算E 32bit -> 48bit
                if action == 'ENCRYPT':
                    temp = self.xor(self.round_keys[i], temp)
                elif action == 'DECRYPT':
                    temp = self.xor(self.round_keys[15-i], temp)  # 解密时轮密钥得反过来
                temp = self.s_subti(temp)  # S-box选择压缩运算 48bit -> 32bit
                temp = self.substi(temp, P)  # P置换
                temp = self.xor(left, temp)  # 与left异或
                left = right
                right = temp
            # 逆初始置换IP_1并将每8个字符加密后的结果连起来
            output += self.substi(right + left, PI_1)
        return bits_to_string(output)

    def substi(self, block, table):  # 进行各种替换
        return [block[x-1] for x in table]

    def expend(self, block, table):
        return self.substi(block, table)

    def key_gener(self):  # 轮密钥生成
        key = string_to_bits(self.key)  # 64bit串
        key = self.substi(key, PC_1)  # PC_1置换 64bit -> 56bit
        left, right = split(key, 28)
        for i in range(16):  # 共16轮迭代
            left, right = self.shift(left, right, SHIFT[i])  # 每轮的循环左移
            self.round_keys.append(self.substi(
                left + right, PC_2))  # PC_2置换后存入对应轮 56bit -> 64bit

    def xor(self, x, y):
        return [a ^ b for a, b in zip(x, y)]

    def s_subti(self, text):  # S-box替换
        subblocks = split(text, 6)  # 每组6bit
        result = []
        for i in range(8):  # 一共8个选择压缩函数
            block = subblocks[i]
            row = int(str(block[0])+str(block[5]), 2)
            column = int(''.join([str(block[i]) for i in range(1, 5)]), 2)
            val = S_BOX[i][row][column]
            bin = binval(val, 4)  # 6bit -> 4bit
            result += [int(x) for x in bin]
        return result

    def shift(self, x, y, n):
        return x[n:]+x[:n], y[n:]+y[:n]

    def encry(self, text, key):
        return self.run(key, text, 'ENCRYPT')

    def decry(self, text, key):
        return self.run(key, text, 'DECRYPT')


if __name__ == '__main__':
    key = '12345678'
    text = 'hihihihi'
    s = DES()
    enc = s.encry(text, key)
    dec = s.decry(enc, key)
    print('cipher: %r' % enc)
    print('plain: %r' % dec)
