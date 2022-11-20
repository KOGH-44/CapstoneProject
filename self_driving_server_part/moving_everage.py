import random
from matplotlib import pyplot as plt

x_vec_array = [] # 무빙 에버리징을 위한 0으로 가득찬 배열 생성 (3개의 평균값을 이용하여 방향 결정 (노이즈 최소화))
x_vec_array_moving_average = []
x_vec_array_default = []
n_frame = []
n = 0
while n < 10:
    x_vec = random.randrange(-50,50)

    x_vec_array.append(x_vec) # 프레임 마다 나오는 x_vec(방향을 위한)값을 배열에 추가
    if len(x_vec_array) is 3 :
        moving_averaging_list_sum = sum(x_vec_array)
        moving_average = moving_averaging_list_sum / 3
        print(x_vec_array)
        x_vec_array.pop(0)
        print(moving_average)
        x_vec_array_default.append(x_vec)
        x_vec_array_moving_average.append(moving_average)
        n_frame.append(n)
    n = n+1

print("***********************************************")
print(x_vec_array_default)
print("***********************************************")
print(x_vec_array_moving_average)
print(n_frame)
plt.plot(n_frame, x_vec_array_default, color = 'red')
plt.plot(n_frame, x_vec_array_moving_average, color = 'green')
plt.show()     
    