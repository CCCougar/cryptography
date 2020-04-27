#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from functools import reduce

Sbox = (
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)

InvSbox = (
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D,
)


Rcon_col = [[0x01, 0x0, 0x0, 0x0],
            [0x02, 0x0, 0x0, 0x0],
            [0x04, 0x0, 0x0, 0x0],
            [0x08, 0x0, 0x0, 0x0],
            [0x10, 0x0, 0x0, 0x0],
            [0x20, 0x0, 0x0, 0x0],
            [0x40, 0x0, 0x0, 0x0],
            [0x80, 0x0, 0x0, 0x0],
            [0x1b, 0x0, 0x0, 0x0],
            [0x36, 0x0, 0x0, 0x0]]

dic = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
       '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}


def str_to_hex(text):
    result = []
    for i in text:
        result.extend([hex(int(char_to_bin(i, 8), 2))])
    return result


def char_to_bin(cha, length=8):
    bin_str = bin(ord(cha))[2:]
    if len(bin_str) > length:
        raise "The character cannot be converted to 8 bits"
    while len(bin_str) < length:
        bin_str = "0" + bin_str
    return "0b"+bin_str


def split(hex_list, length=4):  # 一维转二维
    result = [hex_list[i:i+length] for i in range(0, len(hex_list), length)]
    return result


# def str_to_matrix(text):  # 字符串转化到二维矩阵
#     matrix_1 = split(str_to_hex(text), 4)
    #   matrix_2 = [[0 for _ in range(4)] for _ in range(4)]
    # for i in range(4):
    #     for j in range(4):
    #         matrix_2[i][j] = matrix_1[j][i]

def str_to_matrix(text):
    matrix_1 = split(['0x'+text[i:i+2] for i in range(0, len(text), 2)], 4)
    matrix_2 = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            matrix_2[i][j] = matrix_1[j][i]
    return matrix_2


# def matrix_to_str(matrix):  # 二维矩阵转化到字符串
#     matrix_2 = [[0 for _ in range(4)] for _ in range(4)]
#     for i in range(4):
#         for j in range(4):
#             matrix_2[i][j] = matrix[j][i]
#     result = ''
#     for i in matrix_2:
#         for j in i:
#             result += chr(int(j, 16))
#     return result

def matrix_to_str(matrix):  # 二维矩阵转化到字符串
    matrix_2 = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            matrix_2[i][j] = matrix[j][i]
    result = ''
    for i in matrix_2:
        for j in i:
            if len(j) == 4:
                result += j[2:]
            else:
                result += '0' + j[2:]
    return result


class AES():

    def __init__(self):
        self.key = None
        self.text = None
        self.round_keys = []

    def run(self, text, key, action):
        # self.check(text, key)  # 检查输入
        self.key = key
        self.text = text
        self.round_keys = []
        self.generkeys()
        if action == 'ENCRYPT':
            init_text_matrix, init_key_matrix = str_to_matrix(
                self.text), str_to_matrix(self.key)
            tmp_0 = self.AddRoundKey(
                init_text_matrix, init_key_matrix)  # initial round

            for i in range(9):  # 9 rounds
                tmp_1 = self.ByteSub(tmp_0) if i == 0 else self.ByteSub(tmp_4)
                tmp_2 = self.ShiftRows(tmp_1)
                tmp_3 = self.MixColumn(tmp_2)
                tmp_4 = self.AddRoundKey(tmp_3, self.round_keys[i])

            tmp_5 = self.ByteSub(tmp_4)
            tmp_6 = self.ShiftRows(tmp_5)
            tmp_7 = self.AddRoundKey(tmp_6, self.round_keys[9])
            return matrix_to_str(tmp_7)
        if action == 'DECRYPT':
            init_text_matrix, init_key_matrix = str_to_matrix(
                self.text), str_to_matrix(self.key)
            tmp_0 = self.AddRoundKey(
                init_text_matrix, self.round_keys[9])  # initial round

            for i in range(9):  # 9 rounds
                tmp_1 = self.inv_ShiftRows(
                    tmp_0) if i == 0 else self.inv_ShiftRows(tmp_4)
                tmp_2 = self.inv_ByteSub(tmp_1)
                tmp_3 = self.AddRoundKey(tmp_2, self.round_keys[8-i])
                tmp_4 = self.inv_MixColumn(tmp_3)

            tmp_5 = self.inv_ShiftRows(tmp_4)
            tmp_6 = self.inv_ByteSub(tmp_5)
            tmp_7 = self.AddRoundKey(tmp_6, init_key_matrix)
            return matrix_to_str(tmp_7)

    def AddRoundKey(self, mat1, mat2):
        result = [[0 for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                result[i][j] = (hex(
                    (int(mat1[i][j], 16) ^ int(mat2[i][j], 16))))
        return result

    def ByteSub(self, matrix):
        result = [[] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                if len(matrix[i][j]) == 4:
                    row, col = dic[matrix[i][j][2:3]], dic[matrix[i][j][3:4]]
                else:
                    row, col = 0, dic[matrix[i][j][2:3]]
                result[i].append(hex(Sbox[row*16+col]))
        return result

    def inv_ByteSub(self, matrix):
        result = [[] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                if len(matrix[i][j]) == 4:
                    row, col = dic[matrix[i][j][2:3]], dic[matrix[i][j][3:4]]
                else:
                    row, col = 0, dic[matrix[i][j][2:3]]
                result[i].append(hex(InvSbox[row*16+col]))
        return result

    def ShiftRows(self, matrix):
        for i in range(len(matrix)):
            matrix[i] = matrix[i][i:] + matrix[i][:i]
        return matrix

    def inv_ShiftRows(self, matrix):
        for i in range(len(matrix)):
            matrix[i] = matrix[i][-i:] + matrix[i][:-i]
        return matrix

    def MixColumn(self, matrix):
        for i in range(4):
            column_list = []
            for j in range(4):
                column_list.append(matrix[j][i])
            mixed_column = self.Mix_One_Column(column_list)
            for j in range(4):
                matrix[j][i] = mixed_column[j]
        return matrix

    def Mix_One_Column(self, one_col):
        def xor(x, y): return x ^ y
        def tran_to_int(s): return int(s, 16)
        def Dec_to_hex_str(s): return hex(s)
        one_col = list(map(tran_to_int, one_col))

        def gmul(a, b):
            p = 0
            while a and b:
                if(b & 0x1):
                    p ^= a
                carry = a & 0x80
                a <<= 1
                if(carry):
                    a ^= 0x11b
                b >>= 1
            return p
        new_one_col = []
        new_one_col.append(reduce(xor, [gmul(one_col[0], 0x02),
                                        gmul(one_col[1], 0x03), gmul(one_col[2], 0x01), gmul(one_col[3], 0x01)]))
        new_one_col.append(reduce(xor, [gmul(one_col[0], 0x01),
                                        gmul(one_col[1], 0x02), gmul(one_col[2], 0x03), gmul(one_col[3], 0x01)]))
        new_one_col.append(reduce(xor, [gmul(one_col[0], 0x01),
                                        gmul(one_col[1], 0x01), gmul(one_col[2], 0x02), gmul(one_col[3], 0x03)]))
        new_one_col.append(reduce(xor, [gmul(one_col[0], 0x03),
                                        gmul(one_col[1], 0x01), gmul(one_col[2], 0x01), gmul(one_col[3], 0x02)]))
        new_one_col = list(map(Dec_to_hex_str, new_one_col))
        return new_one_col

    def inv_MixColumn(self, matrix):  # ????????
        for i in range(4):
            column_list = []
            for j in range(4):
                column_list.append(matrix[j][i])
            mixed_column = self.inv_Mix_One_Column(column_list)
            for j in range(4):
                matrix[j][i] = mixed_column[j]
        return matrix

    def inv_Mix_One_Column(self, one_col):
        def xor(x, y): return x ^ y
        def tran_to_int(s): return int(s, 16)
        def Dec_to_hex_str(s): return hex(s)
        one_col = list(map(tran_to_int, one_col))

        def gmul(a, b):
            p = 0
            while a and b:
                if(b & 0x1):
                    p ^= a
                carry = a & 0x80
                a <<= 1
                if(carry):
                    a ^= 0x11b
                b >>= 1
            return p
        new_one_col = []
        new_one_col.append(reduce(xor, [gmul(one_col[0], 0x0e),
                                        gmul(one_col[1], 0x0b), gmul(one_col[2], 0x0d), gmul(one_col[3], 0x09)]))
        new_one_col.append(reduce(xor, [gmul(one_col[0], 0x09),
                                        gmul(one_col[1], 0x0e), gmul(one_col[2], 0x0b), gmul(one_col[3], 0x0d)]))
        new_one_col.append(reduce(xor, [gmul(one_col[0], 0x0d),
                                        gmul(one_col[1], 0x09), gmul(one_col[2], 0x0e), gmul(one_col[3], 0x0b)]))
        new_one_col.append(reduce(xor, [gmul(one_col[0], 0x0b),
                                        gmul(one_col[1], 0x0d), gmul(one_col[2], 0x09), gmul(one_col[3], 0x0e)]))
        new_one_col = list(map(Dec_to_hex_str, new_one_col))
        return new_one_col

    def mul_2(self, num):
        bin_str = bin(num)[2:]
        while len(bin_str) < 8:
            bin_str = '0' + bin_str
        if bin_str[0] == 0:
            bin_str = bin_str[1:] + '0'
        else:  # bin_str[0] == 1
            s = '0b00011011'
            bin_str = bin_str[1:] + '0'
            bin_str = num ^ int(s, 2)
        return bin_str

    def mul_3(self, num):
        bin_str = bin(num)[2:]
        while len(bin_str) < 8:
            bin_str = '0' + bin_str
        s = '0b00000010'
        tmp = int(s, 2) ^ num
        num = tmp ^ num
        return num

    def check(self, text, key):
        if len(text) % 16 != 0 or len(key) != len(text):  # 128 bits
            raise "the length of the text or key does not meet the requirements."
        return

    def ByteSub_column(self, col):
        result = []
        for i in range(4):
            if len(col[i]) == 4:
                row, column = dic[col[i][2:3]], dic[col[i][3:4]]
            else:
                row, column = 0, dic[col[i][2:3]]
            result.append(hex(Sbox[row*16+column]))
        return result

    def make_first_col(self, col_1, col_2, n):
        col = col_1[1:]+col_1[:1]
        col = self.ByteSub_column(col)
        for i in range(4):
            col[i] = hex(int(col_2[i], 16) ^ int(
                col[i], 16) ^ Rcon_col[n][i])  # 类型
        return col

    def make_other_col(self, col_1, col_2):
        col = []
        for i in range(4):
            col.append(hex(int(col_1[i], 16) ^ int(col_2[i], 16)))  # 类型
        return col

    def generkeys(self):
        init_key_matrix = str_to_matrix(self.key)
        self.round_keys.append(init_key_matrix)  # 先把key放入round_key中，后去除
        for i in range(10):
            round_key = [[0 for _ in range(4)] for _ in range(4)]
            col_list = []
            for j in range(4):
                one_col_list = []
                for k in range(4):
                    one_col_list.append(self.round_keys[i][k][j])
                col_list.append(one_col_list)
            round_key_col = [[] for _ in range(4)]
            round_key_col[0] = self.make_first_col(
                col_list[3], col_list[0], i)
            round_key_col[1] = self.make_other_col(
                round_key_col[0], col_list[1])
            round_key_col[2] = self.make_other_col(
                round_key_col[1], col_list[2])
            round_key_col[3] = self.make_other_col(
                round_key_col[2], col_list[3])
            for j in range(4):
                for k in range(4):
                    round_key[j][k] = round_key_col[k][j]
            self.round_keys.append(round_key)
        self.round_keys = self.round_keys[1:]
        return

    def encrypt(self, text, key):
        return self.run(text, key, 'ENCRYPT')

    def decrypt(self, text, key):
        return self.run(text, key, 'DECRYPT')


if __name__ == '__main__':
    s = AES()
    secrt = s.encrypt('00112233445566778899aabbccddeeff',
                      '000102030405060708090a0b0c0d0e0f')  # 暂时只支持138bit的加解密(64位字符串)
    print('密文：%r' % secrt)
    print('明文：%r' % s.decrypt('69c4e0d86a7b0430d8cdb78070b4c55a',
                              '000102030405060708090a0b0c0d0e0f'))
