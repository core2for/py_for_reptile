import random
# 今日作业1：
#    目标：实现字符串的逆序排列
#    思路：用循环做，构建一个新的字符串，从末尾向头取字符串，每次取一个然后添加到后面。

def str_reverse(s):
    result = ''
    for i in range(len(s)-1,-1,-1):
        result += s[i]
    return result

# 思考题目1：
# 	    思路：也是用循环，不能构造新的字符串，通过交换实现。(先把字符串转换成list，然后交换实现，最后再转换成字符串)

def str_reverse2(s):
    str_list = list(s)
    s_len = len(s)
    for i in range(s_len//2):
        temp = str_list[i]
        str_list[i] = str_list[s_len-1-i]
        str_list[s_len-1-i] = temp
    return ''.join(str_list)

# 正确结果测试函数
def reverse_str(s):
    return s[::-1]

# 生成随机字符串
def random_str():
    word_26 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    num = random.randint(1, 100)
    random_str = ''
    for i in range(num):
        index = random.randint(0, 25)
        random_str += word_26[index]
    return random_str

# 测试
def test_str_reverse():
    s = random_str()
    right_str = reverse_str(s)
    my_str = str_reverse(s)
    assert(my_str == right_str)

def test_str_reverse2():
    s = random_str()
    right_str = reverse_str(s)
    my_str = str_reverse2(s)
    assert(my_str == right_str)

if __name__ == '__main__':
    for i in range(1000):
        test_str_reverse()
        test_str_reverse2()
