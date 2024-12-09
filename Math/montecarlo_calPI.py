import random

n = 10000000
inPI_count = 0
# 蒙特卡洛计算圆周率
# PI = lim_{n->inf} 4 * inPI_count / n
# 10000k位才收敛到小数点后两位，这个收敛速度祖冲之手算都算出来了
for i in range(n):
    x = random.random()
    y = random.random()
    if x**2 + y**2 < 1:
        inPI_count = inPI_count + 1

PI_ = 4 * inPI_count / n
print(PI_)
