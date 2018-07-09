import sys
import math


def is_prime(number):
    for i in range(2, int(math.sqrt(number))):
        if number % i == 0:
            return False
    return True


def mannyson_number(find_num=6):
    count = 0
    for num in range(2, sys.maxsize):
        if is_prime(num):
            m = 2**num - 1
            if is_prime(m):
                count += 1
        if count == find_num:
            return m


if __name__ == '__main__':
    print(mannyson_number(6))
