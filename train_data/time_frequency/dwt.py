# dwt_time_frequency.py

import numpy as np
import matplotlib.pyplot as plt
import pywt
import scipy.io

# 加载数据
data = scipy.io.loadmat('signal.mat')
data_signal = data['data_signal'].flatten()

# 设置参数
wavelet_type = 'haar'  # 可选的母小波，如 'haar', 'db1', 'sym2', 'coif1' 等
max_level = pywt.dwt_max_level(len(data_signal), wavelet_type)

sampling_rate = 4e6  # 4 MHz
dt = 1 / sampling_rate
# 进行离散小波变换
coeffs = pywt.wavedec(data_signal, wavelet=wavelet_type, level=max_level)
# 创建一个二维矩阵
coeff_matrix = np.zeros((max_level + 1, len(data_signal)))
for i in range(len(coeffs)):
    coeff_matrix[i, :len(coeffs[i])] = np.abs(coeffs[i])
print(coeff_matrix.shape) #len(data_signal)*(max_level+1) +1表示残差
# 绘制时频图
plt.figure(figsize=(12, 6))
plt.yscale('log')
plt.imshow(coeff_matrix, extent=[0, len(data_signal) * dt, 1, max_level + 2], aspect='auto', cmap='jet')
# 设置色条与标签
plt.colorbar(label='Magnitude')
# 标题和坐标轴标签
plt.title(f'DWT Time-Frequency using {wavelet_type} wavelet')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.grid()

# 保存图像到当前目录
plt.tight_layout()
plt.savefig('DWT_time_frequency.png', bbox_inches='tight')
plt.close()  # 关闭图像，释放内存
