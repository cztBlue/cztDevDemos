import numpy as np

# 蒙特卡罗积分demo

# 被积分函数
def f(x):
    return x**2

def monte_carlo_integration(num_samples=10000000):
    x = np.random.uniform(0, 1, num_samples)
    y = f(x)
    aver = np.mean(y)
    inte = aver * 1  # 区间长度为 1 - 0 = 1
    return inte

# 计算积分
integral = monte_carlo_integration()
print(f"x^2在[0,1]montecarlo积分值: {integral}")