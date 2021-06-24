#include "aes.h"

constexpr auto ENCRY = 1;
constexpr auto DECRY = 0;

void add_new4by4_to_exten(unsigned char *ptr_exten, const unsigned char *ptr_new_matrix, const int col_size);
void copy_matrix(unsigned char *des_matrix, const unsigned char *src_matrix, int matrix_size);
void col2word(unsigned char *des_word, const unsigned char *matrix, int col_ind, int col_num);
void word2col(unsigned char *des_mat, const unsigned char *ptr_word, int col_ind, int col_num);
void Tfunction(unsigned char *, int);
void wordxor(unsigned char *, const unsigned char *, const unsigned char *);
void word_circulation(unsigned char *);
void byte_substitution(unsigned char *);
void XOR_of_round_constant(unsigned char *, int);
void s_box(unsigned char *, int);
void matrix_byte_substitution(unsigned char *, int);
void row_shift(unsigned char *);
void column_mix(unsigned char *, int);
void sub_column_mix(unsigned char *, unsigned char *);
unsigned char mul2(unsigned char);
unsigned char mul3(unsigned char);
unsigned char mul9(unsigned char);
unsigned char mulB(unsigned char);
unsigned char mulD(unsigned char);
unsigned char mulE(unsigned char);
void str2matrix(unsigned char *ptr_str, unsigned char *ptr_matrix, int row_num, int col_num); //使用列指针
void matrix2str(unsigned char *ptr_matrix, unsigned char *ptr_str, int row_num, int col_num);
void decry_sub_column_mix(unsigned char *, unsigned char *);
void decry_row_shift(unsigned char *);
unsigned char mul(unsigned char my_byte1, unsigned char my_byte2);
//void matrix_XOR(unsigned char *ptr_result_matrix, const unsigned char *ptr_matrix_1, const unsigned char *ptr_matrix_2);

extern const unsigned char S_Box[16][16];
extern const unsigned char RE_S_Box[16][16];
extern const unsigned char Rcon[4][10];

AESAlgorithm::AESAlgorithm(const unsigned char *symmetric_key)
{
    //    这个构造函数只从输入中读取16字节
    memcpy(this->sec_key, symmetric_key, 16);
    this->key_exten(); //密钥输入后即进行密钥扩展
}

void AESAlgorithm::enc(unsigned char *ptr_palin)
{
    unsigned char plain_matrix[4][4];
    unsigned char *col_ptr_plain = &plain_matrix[0][0];

    memcpy(this->plain_text, ptr_palin, 4 * 4);
    str2matrix(this->plain_text, col_ptr_plain, 4, 4);
    this->first_key_add(col_ptr_plain); //第一次轮密钥加
    for (int i = 0; i < 10; i++)
    {
        matrix_byte_substitution(col_ptr_plain, ENCRY); //字节代换
        row_shift(col_ptr_plain);                       //行位移
        if (i != 9)
            column_mix(col_ptr_plain, ENCRY);      //列混合, 1代表加密
        this->round_key_add(col_ptr_plain, i + 1); //轮密钥加
    }
    matrix2str(col_ptr_plain, this->cipher_text, 4, 4);
}

void AESAlgorithm::dec(unsigned char *ptr_cipher)
{
    unsigned char cipher_matrix[4][4];
    unsigned char *col_ptr_cipher = &cipher_matrix[0][0];

    memcpy(this->cipher_text, ptr_cipher, 4 * 4);
    str2matrix(this->cipher_text, col_ptr_cipher, 4, 4);
    this->decry_first_key_add(col_ptr_cipher); //第一次轮密钥加
    for (int i = 10; i > 0; i--)
    {
        if (i != 10)
            column_mix(col_ptr_cipher, DECRY);           //逆列混合， 0代表解密
        decry_row_shift(col_ptr_cipher);                 //逆行位移
        matrix_byte_substitution(col_ptr_cipher, DECRY); //逆字节代换
        this->round_key_add(col_ptr_cipher, i - 1);      //轮密钥加
    }
    matrix2str(col_ptr_cipher, this->plain_text, 4, 4);
}

char *AESAlgorithm::ECB_enc(unsigned char *input_plain)
{
    unsigned char group_tmp[16] = {};
    char *ECB_plain = NULL;
    char *ptr_ECB_plain = NULL;
    int group_num = (strlen((const char *)input_plain)) % 16 ? strlen((const char *)input_plain) / 16 + 1 : strlen((const char *)input_plain) / 16; //??????

    ECB_plain = new char[group_num * 16 + 1];
    ptr_ECB_plain = ECB_plain;
    for (int i = 0; i < group_num; i++)
    {
        memset(group_tmp, 0, 16);
        memcpy(group_tmp, input_plain + i * 16, 16);
        this->enc(group_tmp);
        memcpy(ptr_ECB_plain, this->get_cipher(), 32);
        ptr_ECB_plain += 32;
    }
    *ptr_ECB_plain = 0;
    return ECB_plain;
}

char *AESAlgorithm::CBC_enc(unsigned char *input_plain)
{
    unsigned char group_tmp[16] = {};
    unsigned char group_new[16] = {};
    char *CBC_plain = NULL;
    char *ptr_CBC_plain = NULL;
    int group_num = (strlen((const char *)input_plain)) % 16 ? strlen((const char *)input_plain) / 16 + 1 : strlen((const char *)input_plain) / 16; //判断该分多少组

    CBC_plain = new char[group_num * 16 + 1];
    ptr_CBC_plain = CBC_plain;
    memcpy(group_tmp, this->IV, 16); //最开始会和IV向量进行异或
    for (int i = 0; i < group_num; i++)
    {
        memset(group_new, 0, 16);
        memcpy(group_new, input_plain + i * 16, 16); //读入该组的原始明文输入128ibt
        for (int i = 0; i < 16; i++)
        {
            *(group_tmp + i) = *(group_new + i) ^ *(group_tmp + i); //group_tmp执行了该轮的被用来异或的矩阵
        }
        this->enc(group_tmp);                     //基础加密操作
        memcpy(group_tmp, this->cipher_text, 16); //group_tmp保存该组的加密结果，用于下一组解密时的异或
        memcpy(ptr_CBC_plain, this->get_cipher(), 32);
        ptr_CBC_plain += 32;
    }
    *ptr_CBC_plain = 0;
    return CBC_plain;
}

char *AESAlgorithm::ECB_dec(unsigned char *input_cipher)
{
    unsigned char group_tmp[16] = {};
    char *ECB_cipher = NULL;
    char *ptr_ECB_cipher = NULL;
    //    int group_num = strlen((const char*)input_cipher)%16 ? strlen((const char*)input_cipher)/16 + 1 : strlen((const char*)input_cipher)/16;
    int group_num = strlen((const char *)input_cipher) / 16; //密文的长度一定是16byte的整数倍，这里因为依赖了strlen()来判断分组个数，所以输入中的密文必须在末尾包含终结符

    ECB_cipher = new char[group_num * 16 + 1];
    ptr_ECB_cipher = ECB_cipher;
    for (int i = 0; i < group_num; i++)
    {
        memset(group_tmp, 0, 16);
        memcpy(group_tmp, input_cipher + i * 16, 16);
        this->dec(group_tmp);
        memcpy(ptr_ECB_cipher, this->get_plain(), 16);
        ptr_ECB_cipher += 16;
    }
    *ptr_ECB_cipher = 0;
    return ECB_cipher;
}

char *AESAlgorithm::CBC_dec(unsigned char *input_cipher)
{
    unsigned char group_tmp[16] = {};
    unsigned char group_new[16] = {};
    unsigned char tmp_plain[16] = {};

    char *CBC_cipher = NULL;
    char *ptr_CBC_cipher = NULL;
    //    int group_num = strlen((const char*)input_cipher)%16 ? strlen((const char*)input_cipher)/16 + 1 : strlen((const char*)input_cipher)/16;
    int group_num = strlen((const char *)input_cipher) / 16; //密文的长度一定是16byte的整数倍，这里因为依赖了strlen()来判断分组个数，所以输入中的密文必须在末尾包含终结符

    CBC_cipher = new char[group_num * 16 + 1];
    ptr_CBC_cipher = CBC_cipher;
    memcpy(group_tmp, this->IV, 16); //最开始是会先和IV向量进行异或
    for (int i = 0; i < group_num; i++)
    {
        memset(group_new, 0, 16);
        memcpy(group_new, input_cipher + i * 16, 16); //读入该组的原始密文输入128ibt
        this->dec(group_new);                         //对128bit的基本解密操作

        //*******************************
        //将解密结果从成员变量中取出来，然后进行异或
        memcpy(tmp_plain, this->plain_text, 16);
        for (int i = 0; i < 16; i++)
        {
            *(tmp_plain + i) = *(tmp_plain + i) ^ *(group_tmp + i);
        }
        memcpy(this->plain_text, tmp_plain, 16);
        //*******************************

        memcpy(ptr_CBC_cipher, this->get_plain(), 16);   ////这里修改之前取到的明文是没有经过上面的异或的
        memcpy(group_tmp, input_cipher + i * 16, 4 * 4); //group_tmp保存该组的输入，用于下一组解密时的异或
        ptr_CBC_cipher += 16;
    }
    *ptr_CBC_cipher = 0;
    return CBC_cipher;
}

void AESAlgorithm::key_exten()
{
    unsigned char next4by4matrix[4][4];
    unsigned char old4by4matrix[4][4];
    unsigned char *col_ptr_next4by4 = &next4by4matrix[0][0];
    unsigned char *col_ptr_old4by4 = &old4by4matrix[0][0];
    unsigned char old4bytes[4];
    unsigned char new4bytes[4];
    unsigned char xor4bytes[4];
    unsigned char *save_ptr;

    save_ptr = this->col_ptr_exten;
    str2matrix(this->sec_key, col_ptr_next4by4, 4, 4); //弄好最初的一组，前128bit，（使用列指针）
    copy_matrix(col_ptr_old4by4, col_ptr_next4by4, 4 * 4);
    add_new4by4_to_exten(this->col_ptr_exten, col_ptr_next4by4, 4 * 11); //将所有新生成的128扩展密钥加入到这个矩阵中
    for (int i = 0; i < 10; i++)
    { //循环生成11组128bits的扩展密钥，前面已生成一组
        for (int k = 0; k < 4; k++)
        { //按照4个字来处理
            col2word(old4bytes, col_ptr_old4by4, k, 4);
            col2word(xor4bytes, col_ptr_next4by4, (k + 3) % 4, 4);
            if (k == 0) //第一个比较特殊
                Tfunction(xor4bytes, i + 1);
            wordxor(new4bytes, old4bytes, xor4bytes);
            word2col(col_ptr_next4by4, new4bytes, k, 4);
        }
        this->col_ptr_exten += 4;
        add_new4by4_to_exten(this->col_ptr_exten, col_ptr_next4by4, 4 * 11);
        copy_matrix(col_ptr_old4by4, col_ptr_next4by4, 4 * 4);
    }
    this->col_ptr_exten = save_ptr;
}

char *AESAlgorithm::get_cipher()
{
    //unsigned char 转到 16 进制后输出
    char *result = NULL;
    char *ptr = NULL;
    unsigned char temp_byte;
    char high4bit;
    char low4bit;
    //输出里面有32个char，不知道应该包括后面的终结符吗

    result = new char[40];
    memset(result, 0, 40);
    ptr = result;
    for (int i = 0; i < 16; i++)
    {
        temp_byte = *((this->cipher_text) + i);
        high4bit = (temp_byte & 0xf0) / 0x10;
        low4bit = temp_byte & 0xf;
        if (high4bit >= 0 && high4bit < 10)
            *ptr = high4bit + 48;
        else
            *ptr = (high4bit - 0xa) + 0x41;
        if (low4bit >= 0 && low4bit < 10)
            *(ptr + 1) = low4bit + 48;
        else
            *(ptr + 1) = (low4bit - 0xa) + 0x41;
        ptr = ptr + 2;
    }
    *ptr = 0;
    return result;
}

char *AESAlgorithm::get_plain()
{
    char *result = NULL;
    char *ptr = NULL;

    result = new char[20];
    memset(result, 0, 20);
    ptr = (char *)&this->plain_text[0]; //也许会有精度损失，但是在plain text里面应该都是可打印字符，所有应该不会有精度损失
    for (int i = 0; i < 16; i++)
    {
        *(result + i) = *ptr;
        ptr++;
    }
    *ptr = 0;
    return result;
}

void str2matrix(unsigned char *ptr_str, unsigned char *ptr_matrix, int row_num, int col_num)
{
    unsigned char temp_matrix[4][4]; //这里temp_matrix是行指针

    memcpy(*temp_matrix, ptr_str, row_num * col_num); //行指针转化到列指针
    for (int i = 0; i < row_num; i++)
    {
        for (int j = 0; j < col_num; j++)
        {
            *(ptr_matrix + col_num * i + j) = temp_matrix[j][i]; //memcpy赋值后的矩阵再来个转置
        }
    }
    return;
}

void matrix2str(unsigned char *ptr_matrix, unsigned char *ptr_str, int row_num, int col_num)
{
    for (int i = 0; i < row_num; i++)
    {
        for (int j = 0; j < col_num; j++)
        {
            *(ptr_str + row_num * i + j) = *(ptr_matrix + col_num * j + i);
        }
    }
}

void copy_matrix(unsigned char *des_matrix, const unsigned char *src_matrix, int matrix_size)
{
    for (int i = 0; i < matrix_size; i++)
    {
        *(des_matrix + i) = *(src_matrix + i);
    }
    return;
}

void add_new4by4_to_exten(unsigned char *ptr_exten, const unsigned char *ptr_new_matrix, const int col_size)
{
    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            *(ptr_exten + i * col_size + j) = *(ptr_new_matrix + i * 4 + j);
        }
    }
}

void col2word(unsigned char *des_word, const unsigned char *matrix, int col_ind, int col_num)
{
    for (int i = 0; i < 4; i++)
        memcpy(des_word + i, matrix + col_num * i + col_ind, 1);
    return;
}

void word2col(unsigned char *des_mat, const unsigned char *ptr_word, int col_ind, int col_num)
{
    for (int i = 0; i < 4; i++)
        memcpy(des_mat + col_num * i + col_ind, ptr_word + i, 1);
    return;
}

void Tfunction(unsigned char *theword, int round)
{
    //函数参数theword是指向含有4个unsigned char类型数组的指针
    word_circulation(theword);             //字循环
    byte_substitution(theword);            //字节代换
    XOR_of_round_constant(theword, round); //轮常量异或
    return;
}

void wordxor(unsigned char *result_word, const unsigned char *word1, const unsigned char *word2)
{
    for (int i = 0; i < 4; i++)
        *(result_word + i) = *(word1 + i) ^ *(word2 + i);
    return;
}

void word_circulation(unsigned char *theword)
{
    unsigned char tempword[4];

    memcpy(tempword, theword, 4);
    for (int i = 0; i < 4; i++)
        *(theword + i) = *(tempword + (i + 1) % 4);
    return;
}

void byte_substitution(unsigned char *theword)
{
    unsigned char tmp_byte[1];

    for (int i = 0; i < 4; i++)
    {
        *tmp_byte = *(theword + i);
        s_box(tmp_byte, ENCRY);
        *(theword + i) = *tmp_byte;
    }
    return;
}

void s_box(unsigned char *thebyte, int en_de)
{
    int high4bit = ((*thebyte) & 0xf0) / 0x10;
    int low4bit = (*thebyte) & 0x0f;

    if (en_de == ENCRY)
        *thebyte = S_Box[high4bit][low4bit];
    if (en_de == DECRY)
        *thebyte = RE_S_Box[high4bit][low4bit];
}

void XOR_of_round_constant(unsigned char *theword, int round)
{
    unsigned char temp_word[4];
    unsigned char temp_word_Rcon[4];

    col2word(temp_word_Rcon, &Rcon[0][0], round - 1, 10);
    wordxor(temp_word, theword, temp_word_Rcon);
    memcpy(theword, temp_word, 4);
    return;
}

void AESAlgorithm::first_key_add(unsigned char *ptr_plain_ma)
{
    this->round_key_add(ptr_plain_ma, 0);
}

void AESAlgorithm::decry_first_key_add(unsigned char *ptr_plain_ma)
{
    this->round_key_add(ptr_plain_ma, 10);
}

void AESAlgorithm::round_key_add(unsigned char *ptr_plain_ma, int round)
{
    unsigned char plain_word[4];
    unsigned char xor_word[4];
    unsigned char temp_word[4];

    for (int i = 0; i < 4; i++)
    {
        col2word(plain_word, ptr_plain_ma, i, 4);
        col2word(xor_word, (this->col_ptr_exten) + round * 4, i, 4 * 11);
        wordxor(temp_word, plain_word, xor_word);
        word2col(ptr_plain_ma, temp_word, i, 4);
    }
}

void matrix_byte_substitution(unsigned char *ptr_matrix, int en_de)
{
    unsigned char theword[4];

    for (int i = 0; i < 4; i++)
    {
        col2word(theword, ptr_matrix, i, 4);
        for (int k = 0; k < 4; k++)
        {
            if (en_de == ENCRY)
                s_box(theword + k, ENCRY);
            if (en_de == DECRY)
                s_box(theword + k, DECRY);
        }
        word2col(ptr_matrix, theword, i, 4);
    }
    return;
}

void row_shift(unsigned char *ptr_matrix)
{
    unsigned char temp_word[4];

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            temp_word[j] = *(ptr_matrix + i * 4 + j);
        }
        for (int k = 0; k < 4; k++)
        {
            *(ptr_matrix + i * 4 + k) = temp_word[(k + i) % 4];
        }
    }
}

void decry_row_shift(unsigned char *ptr_matrix)
{
    unsigned char temp_word[4];

    for (int i = 0; i < 4; i++)
    {
        for (int j = 0; j < 4; j++)
        {
            temp_word[j] = *(ptr_matrix + i * 4 + j);
        }
        for (int k = 0; k < 4; k++)
        {
            *(ptr_matrix + i * 4 + k) = temp_word[(k + 4 - i) % 4];
        }
    }
}

void column_mix(unsigned char *ptr_matrix, int en_de)
{
    unsigned char plain_word[4];
    unsigned char result_word[4];

    for (int i = 0; i < 4; i++)
    {
        col2word(plain_word, ptr_matrix, i, 4);
        if (en_de == ENCRY)
            sub_column_mix(result_word, plain_word);
        else
            decry_sub_column_mix(result_word, plain_word);
        word2col(ptr_matrix, result_word, i, 4);
    }
}

void sub_column_mix(unsigned char *result_word, unsigned char *plain_word)
{
    *(result_word + 0) = mul2(*(plain_word + 0)) ^ mul3(*(plain_word + 1)) ^ *(plain_word + 2) ^ *(plain_word + 3);
    *(result_word + 1) = *(plain_word + 0) ^ mul2(*(plain_word + 1)) ^ mul3(*(plain_word + 2)) ^ *(plain_word + 3);
    *(result_word + 2) = *(plain_word + 0) ^ *(plain_word + 1) ^ mul2(*(plain_word + 2)) ^ mul3(*(plain_word + 3));
    *(result_word + 3) = mul3(*(plain_word + 0)) ^ *(plain_word + 1) ^ *(plain_word + 2) ^ mul2(*(plain_word + 3));
}

void decry_sub_column_mix(unsigned char *result_word, unsigned char *plain_word)
{
    *(result_word + 0) = mulE(*(plain_word + 0)) ^ mulB(*(plain_word + 1)) ^ mulD(*(plain_word + 2)) ^ mul9(*(plain_word + 3));
    *(result_word + 1) = mul9(*(plain_word + 0)) ^ mulE(*(plain_word + 1)) ^ mulB(*(plain_word + 2)) ^ mulD(*(plain_word + 3));
    *(result_word + 2) = mulD(*(plain_word + 0)) ^ mul9(*(plain_word + 1)) ^ mulE(*(plain_word + 2)) ^ mulB(*(plain_word + 3));
    *(result_word + 3) = mulB(*(plain_word + 0)) ^ mulD(*(plain_word + 1)) ^ mul9(*(plain_word + 2)) ^ mulE(*(plain_word + 3));
}

unsigned char mul(unsigned char my_byte1, unsigned char my_byte2)
{
    unsigned int x = my_byte1, y = my_byte2, answer = 0, decrease, compare;
    for (int i = 0; i < 8; i++)
    {
        if (y & 0x01)
            answer = answer ^ x;
        y = y >> 1;
        x = x << 1;
    }
    decrease = 0B1000110110000000;
    compare = 0x8000;
    for (int i = 0; i < 8; i++)
    {
        if (answer & compare)
            answer = answer ^ decrease;
        decrease = decrease >> 1;
        compare = compare >> 1;
    }
    //    if ((answer & 0xFF00) != 0)
    //        cout << "Error!";
    return answer;
}

unsigned char mul2(unsigned char my_byte)
{
    int a7 = (my_byte & 0x80); //判断最高位是否为0
    int result_byte;

    if (a7 == 0)
    {
        result_byte = my_byte << 1; //往左边移动一位，右边移进0
    }
    else
    {
        result_byte = (my_byte << 1) ^ 0x1b; //往左边移动一位后与00011011异或
    }
    //    if ((result_byte & 0xff) != mul(my_byte, 0X02))
    //        qDebug() << "Error!";
    return result_byte;
}

unsigned char mul3(unsigned char my_byte)
{
    int result_byte;

    result_byte = mul2(my_byte);
    result_byte = result_byte ^ my_byte;
    //    if ((result_byte & 0xff) != mul(0x03, my_byte))
    //        qDebug() << "Error!";
    return result_byte;
}

unsigned char mul9(unsigned char my_byte)
{
    return mul(my_byte, 0x9);
}

unsigned char mulB(unsigned char my_byte)
{
    return mul(my_byte, 0xB);
}

unsigned char mulD(unsigned char my_byte)
{
    return mul(my_byte, 0xD);
}

unsigned char mulE(unsigned char my_byte)
{
    return mul(my_byte, 0xE);
}

//void matrix_XOR(unsigned char *ptr_result_matrix, const unsigned char *ptr_matrix_1, const unsigned char *ptr_matrix_2){
//    unsigned char plain_word[4];
//    unsigned char xor_word[4];
//    unsigned char temp_word[4];

//    for(int i = 0; i < 4; i++){
//        col2word(plain_word, ptr_matrix_1, i, 4);
//        col2word(xor_word, ptr_matrix_2, i, 4);
//        wordxor(temp_word, plain_word, xor_word);
//        word2col(ptr_result_matrix, temp_word, i, 4);
//    }
//}
